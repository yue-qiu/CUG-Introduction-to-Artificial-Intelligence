# CUG Introduction to Artificial Intelligence

这个 repo 是 2020 Fall 中国地质大学（武汉）计算机学院赵曼老师《人工智能导论》课的期末上机内容。一共包含五个题目：

- 分别采用随机重启爬山法、最小冲突法和遗传算法求解 N 皇后问题
- 使用联机搜索求解 Wumpus 怪兽世界问题
- 采用α-β 剪枝算法实现井字棋游戏
- 采用粒子群算法求解函数 $y = f(x_1, x_2) =x_1^2 - x_2^2$  的最小值，其中 $-10 \leq x_1, x_2 \leq 10$
- 利用遗传算法求解函数 $f(x) = 15x - x^2; x \in [0, 15], x \in Z$ 时的最大值

理论上是要求有图形化界面的，由于本人宁愿扣分也不想花时间在画 GUI 上所以全部用命令行来实现。命令行才是程序员的浪漫 :-)

tips: 如果发现本文数学公式渲染有问题，这是因为 GitHub 不支持直接在 Markdown 里插入公式。如果你使用的是 Chrome 浏览器，安装 [这个插件](https://chrome.google.com/webstore/detail/github-with-mathjax/ioemnmodlmafdkllaclgeombjnmnbima/related) 可以解决问题，当然，需要科学上网。
## 三种方案解决 N 皇后问题

为了便于计算这里取 N = 8，但是算法是支持任意整数 N 的。这里给出运行结果截图：

![八皇后截图](https://i.loli.net/2021/01/02/fKI3JuCZS5iGmXO.png)

## 实现 Wumpus World 游戏

性能量度: gold +1000, death -1000，-1 per step

环境描述：

- Squares adjacent to wumpus are smelly
- Squares adjacent to pit are breezy
- Glitter if gold is in the same square
- Grabbing picks up gold if in same square

地图保存在 `world.txt` 里。地图上有一个 wumpus 和若干个 pit。当然这个规则要靠地图设计者自己保证。

wumpus 四周的房间会散发 stench，pit 四周的房间会发出 breeze。agent 走到某个房间里才能感知到 stench 或 breeze。

agent 根据运动时获得的信息推断 wumpus 和 pit 的位置并保持规避，只在绝对安全或者没有探险过的房间中移动。找到 gold 或者无路可走就原路返回。往未去过的房间移动时可能会遇到 Wumpus 或 pit 导致死亡。

在这张地图中：

```
4 4
A 3 0
W 1 0
G 1 1
P 0 3
P 1 2
P 3 2
```

![找到gold](https://i.loli.net/2021/01/03/ia5nGpNzltgyedC.png)

而在这张地图中，agent 在出生点就感受到了 breeze，游戏直接结束：

```
4 4
A 3 0
W 1 0
G 1 1
P 0 3
P 1 2
P 3 1
```

![没找到gold](https://i.loli.net/2021/01/03/gd9RXBJucwT5IlZ.png)

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
