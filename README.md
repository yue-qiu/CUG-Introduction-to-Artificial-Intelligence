<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      processEscapes: true
    }
  });
</script>

<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

# CUG Introduction to Artificial Intelligence

这个 repo 是 2020 Fall 中国地质大学（武汉）计算机学院赵曼老师《人工智能导论》课的期末上机内容。一共包含五个题目：

- 分别采用随机重启爬山法、最小冲突法和遗传算法求解 N 皇后问题
- 使用联机搜索求解 Wumpus 怪兽世界问题
- 采用α-β 剪枝算法实现井字棋游戏
- 采用粒子群算法求解函数 $y = f(x_1, x_2) =x_1^2 - x_2^2$  的最小值，其中 $-10 \leq x_1, x_2 \leq 10$
- 利用遗传算法求解函数 $f(x) = 15x - x^2; x \in [0, 15], x \in Z$ 时的最大值

理论上是要求有图形化界面的，由于本人宁愿扣分也不想花时间在画 GUI 上所以全部用命令行来实现。命令行才是程序员的浪漫 :-)

## 三种方案解决 N 皇后问题

为了便于计算这里取 N = 8，但是算法是支持任意整数 N 的。这里给出运行结果截图：

![八皇后截图](https://i.loli.net/2021/01/02/fKI3JuCZS5iGmXO.png)

## 实现 Wumpus World 游戏

地图保存在 `world.txt` 里。地图上有一个 wumpus 和若干个 pit。当然这个规则也要靠地图设计者自己保证。

wumpus 四周的房间会散发 stench，pit 四周的房间会发出 breeze。agent 走到某个房间里才能感知到 stench 或 breeze。

agent 根据运动时获得的信息推断 wumpus 和 pit 的位置并一直规避。找到 gold 或者在确保自己安全的情况下无路可走就原路返回。

分数计算公式：

```
Score = 1000 * gold - step
```

![wumpus](https://i.loli.net/2021/01/02/kU4FZq8OyQY9jWl.png)

## $\alpha$-$\beta$ 剪枝法实现井字棋人机对弈

玩家落子的时候没有做可行检测，所以要自己注意不要再非空地上落子否则会发生覆盖。

玩家可以自由选择先后：

![选择先后手](https://i.loli.net/2021/01/02/h9i8QkmLzUo5KuC.png)

落子时行列以一个空格分割：

![落子](https://i.loli.net/2021/01/02/NoX4D5Yaq3ySTHk.png)

游戏一共有三种结局：玩家胜利、AI 胜利和平局

## 粒子群法求解函数极小值

这里给出一个[粒子群算法的讲解](https://blog.csdn.net/saltriver/article/details/63680364)。

![PSO运行结果](https://i.loli.net/2021/01/02/LubAYMNOkCaBEVh.png)

## 遗传算法求解函数极大值

遗传算法个人觉得蛮有意思的，模拟了自然界选择配偶、杂交和变异的过程。整个过程中以适应度为标准不断更新种群，结果就是整个种群越来越好，直到满足了我们预设的标准。

![GA运行结果](https://i.loli.net/2021/01/02/SJI13ghQvGAtbfY.png)
