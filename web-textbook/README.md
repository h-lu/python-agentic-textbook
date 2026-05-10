# Python 教材网站

《Python 程序设计（Agentic Coding）》交互式网站版本。

## 特性

- 📚 **14 周完整课程** - 从入门基础到综合实战
- 🎨 **现代响应式设计** - 移动端友好
- 📝 **可折叠代码块** - Python 代码默认折叠，支持一键复制
- 🔍 **章节导航** - 自动从标题生成目录
- ⬅️➡️ **前后导航** - 章节间轻松切换

## 技术栈

- **框架**: Next.js 15 (React 19)
- **样式**: Tailwind CSS
- **渲染**: react-markdown + remark-gfm
- **组件**: Radix UI Collapsible
- **构建**: 静态导出 (output: 'export')

## 开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问 http://localhost:3000
```

## 构建

```bash
# 构建静态网站（会先生成 .structure-cache.json）
npm run build

# 构建产物在 out/ 目录
```

## 部署

支持任何静态托管服务：

### Vercel

```bash
vercel deploy
```

### Netlify

将 `out/` 目录连接到 Netlify 即可。

### 其他

- GitHub Pages
- Cloudflare Pages
- AWS S3 + CloudFront

## 项目结构

```
├── src/
│   ├── app/              # Next.js App Router
│   │   ├── page.tsx      # 首页（课程概览）
│   │   ├── layout.tsx    # 根布局
│   │   ├── globals.css   # 全局样式
│   │   └── week-*/       # 章节页面
│   ├── components/       # React 组件
│   │   ├── collapsible-code.tsx  # 可折叠代码块
│   │   ├── chapter-nav.tsx      # 章节导航
│   │   └── chapter-footer.tsx   # 前后导航
│   └── lib/             # 工具库
│       └── design-system.ts     # 设计系统
├── public/
│   └── chapters/        # Markdown 源文件
└── .structure-cache.json  # 构建时自动生成的章节元数据缓存
```

## 课程阶段

| 阶段 | 周次 | 主题 |
|------|------|------|
| 入门基础 | 01-05 | 变量、控制流、函数、容器、文件 |
| 工程进阶 | 06-10 | 异常、模块、测试、文本、JSON |
| 综合实战 | 11-14 | dataclass、CLI、Agent 协作、发布 |

## License

与原教材保持一致。
