python -m referee -v1 -l logs/sample/red_greedy.txt player.mix player.fixed_greedy player.fixed_greedy
python -m referee -v1 -l logs/sample/green_greedy.txt player.fixed_greedy player.mix player.fixed_greedy
python -m referee -v1 -l logs/sample/blue_greedy.txt player.fixed_greedy player.fixed_greedy player.mix

python -m referee -v1 -l logs/sample/red_runner.txt player.mix player.fixed_runner player.fixed_runner
python -m referee -v1 -l logs/sample/green_runner.txt player.fixed_runner player.mix player.fixed_runner
python -m referee -v1 -l logs/sample/blue_runner.txt player.fixed_runner player.fixed_runner player.mix

python -m referee -v1 -l logs/sample/red_slow.txt player.mix player.fixed_slow player.fixed_slow
python -m referee -v1 -l logs/sample/green_slow.txt player.fixed_slow player.mix player.fixed_slow
python -m referee -v1 -l logs/sample/blue_slow.txt player.fixed_slow player.fixed_slow player.mix

cd '.\logs\sample'

python results.py

$SHELL