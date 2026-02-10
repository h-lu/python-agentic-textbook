import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Python 程序设计（Agentic Coding）',
  description: '面向零基础的 Python 编程教材，采用 Agentic Coding 方法论',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-screen bg-neutral-50">
        {children}
      </body>
    </html>
  )
}
