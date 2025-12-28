#!/usr/bin/env python
"""
简单的100局游戏基准测试脚本
"""
import time
import sys
from fireplace import cards
from fireplace.exceptions import GameOver
from fireplace.utils import play_full_game


def run_benchmark(num_games=100):
    """运行指定数量的游戏并统计时间"""
    print(f"开始运行 {num_games} 局游戏...")
    print("=" * 60)
    
    # 初始化卡牌数据库
    cards.db.initialize()
    
    successful_games = 0
    failed_games = 0
    game_times = []
    
    total_start = time.time()
    
    for i in range(num_games):
        game_start = time.time()
        
        try:
            play_full_game()
            successful_games += 1
            game_time = time.time() - game_start
            game_times.append(game_time)
            
            # 每10局显示一次进度
            if (i + 1) % 10 == 0:
                avg_so_far = sum(game_times) / len(game_times)
                print(f"进度: {i + 1}/{num_games} 局 | "
                      f"当前局耗时: {game_time:.3f}秒 | "
                      f"平均耗时: {avg_so_far:.3f}秒")
        
        except GameOver:
            # 正常游戏结束
            successful_games += 1
            game_time = time.time() - game_start
            game_times.append(game_time)
            
            if (i + 1) % 10 == 0:
                avg_so_far = sum(game_times) / len(game_times)
                print(f"进度: {i + 1}/{num_games} 局 | "
                      f"当前局耗时: {game_time:.3f}秒 | "
                      f"平均耗时: {avg_so_far:.3f}秒")
        
        except Exception as e:
            failed_games += 1
            print(f"第 {i + 1} 局出错: {e}")
    
    total_time = time.time() - total_start
    
    # 统计结果
    print("\n" + "=" * 60)
    print("基准测试结果:")
    print("=" * 60)
    print(f"总游戏数:     {num_games} 局")
    print(f"成功完成:     {successful_games} 局")
    print(f"失败:         {failed_games} 局")
    print(f"成功率:       {successful_games/num_games*100:.1f}%")
    print("-" * 60)
    print(f"总耗时:       {total_time:.2f} 秒")
    print(f"平均每局:     {sum(game_times)/len(game_times):.3f} 秒")
    print(f"最快一局:     {min(game_times):.3f} 秒")
    print(f"最慢一局:     {max(game_times):.3f} 秒")
    print(f"每秒游戏数:   {num_games/total_time:.2f} 局/秒")
    print("=" * 60)
    
    return {
        'total_games': num_games,
        'successful': successful_games,
        'failed': failed_games,
        'total_time': total_time,
        'avg_time': sum(game_times) / len(game_times),
        'min_time': min(game_times),
        'max_time': max(game_times),
        'games_per_second': num_games / total_time
    }


if __name__ == "__main__":
    num_games = 100
    
    # 如果命令行提供了参数，使用该参数
    if len(sys.argv) > 1:
        try:
            num_games = int(sys.argv[1])
        except ValueError:
            print(f"错误: '{sys.argv[1]}' 不是有效的数字")
            print(f"用法: python {sys.argv[0]} [游戏数量]")
            sys.exit(1)
    
    run_benchmark(num_games)

