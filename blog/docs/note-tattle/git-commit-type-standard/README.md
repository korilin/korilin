---
title: git commit 类型规范记录
date: 2021-12-4
---

来实习的时候发现同事提交的 commit 中有一个前缀，查了一下这是 git commit 的规范之一，因此在这里做个记录。

| type | desc |
| :-: | :-: |
| feat | 新功能 |
| fix | 修复bug |
| docs | 文档改变 |
| style | 代码格式改变 |
| refactor | 某个已有功能重构 |
| perf | 性能优化 |
| test | 增加测试 |
| build | 改变了build工具 如 grunt换成了 npm |
| revert | 撤销上一次的 commit |
| chore | 构建过程或辅助工具的变动 |

使用体验：后面发现这规范其实还挺不错的，用熟悉了可以直接从 commit 的 title 描述中了解到该次 commit 代码都发生了哪些变化。

<!-- more -->
