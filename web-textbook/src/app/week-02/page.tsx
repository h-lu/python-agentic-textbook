import Link from 'next/link'
import fs from 'fs'
import path from 'path'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { ChapterFooter } from '@/components/chapter-footer'
import { CleanCodeBlock } from '@/components/clean-code-block'
import { CleanSidebar } from '@/components/clean-sidebar'

function extractSections(content: string): string[] {
  return content.match(/^##\s+(.+)$/gm)?.map(s => s.replace(/^##\s+/, '')) || []
}

function removeHtmlComments(content: string): string {
  return content.replace(/<!--[\s\S]*?-->/g, '')
}

export default async function Week2Page() {
  const contentPath = path.join(process.cwd(), 'public', 'chapters', 'week-02.md')
  const rawContent = fs.readFileSync(contentPath, 'utf-8')
  const content = removeHtmlComments(rawContent)
  const sections = extractSections(content)

  const cachePath = path.join(process.cwd(), '.structure-cache.json')
  const data = JSON.parse(fs.readFileSync(cachePath, 'utf-8'))
  const currentIndex = data.chapters.findIndex((c: any) => c.week === '02')

  return (
    <div className="min-h-screen bg-white">
      <header className="bg-slate-900 text-white py-12">
        <div className="max-w-4xl mx-auto px-4">
          <Link 
            href="/" 
            className="inline-flex items-center gap-2 text-slate-400 hover:text-white mb-4 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            返回首页
          </Link>
          <h1 className="text-3xl md:text-4xl font-bold">{data.chapters[currentIndex]?.title || 'Week 2'}</h1>
        </div>
      </header>

      {/* Sidebar and Content layout */}
      <div className="flex">
        {/* Floating Sidebar - handles both mobile and desktop */}
        <CleanSidebar sections={sections} />

        {/* Main content */}
        <main className="flex-1 min-w-0 px-4 py-10 lg:py-10 lg:px-8">
          <div className="max-w-4xl mx-auto">
            <article className="prose prose-lg max-w-none">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  h2({ children }) {
                    const text = String(children || '')
                    const sectionIndex = sections.findIndex(s => s === text)
                    const sectionId = sectionIndex >= 0 ? `section-${sectionIndex}` : ''
                    return <h2 id={sectionId}>{children}</h2>
                  },
                  h3({ children }) {
                    return <h3>{children}</h3>
                  },
                  code(props: any) {
                    const { children, className, node, ...rest } = props
                    const match = /language-(\w+)/.exec(className || '')
                    const language = match ? match[1] : 'text'
                    const inline = !className

                    if (!inline && language === 'python') {
                      return (
                        <CleanCodeBlock
                          code={String(children).replace(/\n$/, '')}
                          language="python"
                        />
                      )
                    }

                    return <code className={className} {...rest}>{children}</code>
                  }
                }}
              >
                {content}
              </ReactMarkdown>
            </article>

            <ChapterFooter
              prevChapter={currentIndex > 0 ? data.chapters[currentIndex - 1] : undefined}
              nextChapter={currentIndex < data.chapters.length - 1 ? data.chapters[currentIndex + 1] : undefined}
            />
          </div>
        </main>
      </div>

      {/* Mobile bottom spacer for floating sidebar */}
      <div className="lg:hidden h-20" />
    </div>
  )
}
