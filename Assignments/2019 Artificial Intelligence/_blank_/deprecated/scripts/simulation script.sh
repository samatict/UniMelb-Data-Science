for ((i=0; i<50; i++))
    do
        python -m referee -v0 -l logs/red/red_greedy_$i.txt player.mix player.greedy player.greedy
        python -m referee -v0 -l logs/green/green_greedy_$i.txt player.greedy player.mix player.greedy
        python -m referee -v0 -l logs/blue/blue_greedy_$i.txt player.greedy player.greedy player.mix
    done

for ((i=0; i<50; i++))
    do
    python -m referee -v0 -l logs/red/red_paranoid_$i.txt player.mix player.runner player.runner
    python -m referee -v0 -l logs/green/green_paranoid_$i.txt player.runner player.mix player.runner
    python -m referee -v0 -l logs/blue/blue_paranoid_$i.txt player.runner player.runner player.mix
    done

for ((i=0; i<50; i++))
    do
    python -m referee -v0 -l logs/red/red_maxn_$i.txt player.mix player.slow player.slow
    python -m referee -v0 -l logs/green/green_maxn_$i.txt player.slow player.mix player.slow
    python -m referee -v0 -l logs/blue/blue_maxn_$i.txt player.slow player.slow player.mix
    done