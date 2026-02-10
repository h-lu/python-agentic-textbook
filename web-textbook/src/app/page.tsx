import Link from 'next/link'
import fs from 'fs'
import path from 'path'

interface Chapter {
  week: string
  title: string
  file: string
  sections: string[]
  code_blocks: number
}

interface SyllabusData {
  syllabus: {
    title: string
    stages: Array<{
      name: string
      weeks: string[]
    }>
  }
  chapters: Chapter[]
}

async function getSyllabusData(): Promise<SyllabusData> {
  const cachePath = path.join(process.cwd(), '.structure-cache.json')
  const data = fs.readFileSync(cachePath, 'utf-8')
  return JSON.parse(data)
}

export default async function HomePage() {
  const { syllabus, chapters } = await getSyllabusData()

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-gradient-to-br from-primary-600 to-primary-800 text-white">
        <div className="max-w-6xl mx-auto px-4 py-16 md:py-24">
          <div className="text-center">
            <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur px-4 py-2 rounded-full mb-6">
              <span className="text-yellow-300">🐍</span>
              <span className="text-sm font-medium">面向零基础 · AI 时代的编程入门</span>
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4 text-balance">
              {syllabus.title}
            </h1>
            <p className="text-xl md:text-2xl text-primary-100 max-w-3xl mx-auto text-balance">
              用"工程化 + Agentic 工作流"掌握 Python 基本功
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              <div className="flex items-center gap-2 bg-white/10 px-4 py-2 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                <span>14 周完整课程</span>
              </div>
              <div className="flex items-center gap-2 bg-white/10 px-4 py-2 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
                <span>实战项目驱动</span>
              </div>
              <div className="flex items-center gap-2 bg-white/10 px-4 py-2 rounded-lg">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                <span>AI 辅助编程</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Learning Stages */}
      <section className="py-16 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-neutral-900 mb-12">学习路径</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {syllabus.stages.map((stage, idx) => (
              <div
                key={idx}
                className="relative p-6 rounded-xl border-2 border-neutral-200 hover:border-primary-300 transition-colors"
              >
                <div className="absolute -top-3 -left-3 w-10 h-10 bg-primary-500 text-white rounded-full flex items-center justify-center font-bold">
                  {idx + 1}
                </div>
                <h3 className="text-xl font-semibold text-neutral-900 mb-2">{stage.name}</h3>
                <div className="flex flex-wrap gap-2 mt-4">
                  {stage.weeks.map(week => (
                    <span
                      key={week}
                      className="text-sm bg-neutral-100 text-neutral-600 px-3 py-1 rounded-full"
                    >
                      Week {week}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Chapter Grid */}
      <section className="py-16 bg-neutral-50">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-neutral-900 mb-12">课程章节</h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {chapters.map(chapter => (
              <Link
                key={chapter.week}
                href={`/week-${chapter.week}`}
                className="group p-5 bg-white rounded-lg border border-neutral-200 hover:border-primary-400 hover:shadow-lg transition-all"
              >
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-sm font-mono bg-primary-100 text-primary-700 px-2 py-1 rounded">
                    {chapter.week.padStart(2, '0')}
                  </span>
                  {chapter.code_blocks > 0 && (
                    <span className="text-xs text-neutral-500 flex items-center gap-1">
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                      </svg>
                      {chapter.code_blocks}
                    </span>
                  )}
                </div>
                <h3 className="font-medium text-neutral-900 group-hover:text-primary-600 transition-colors line-clamp-2">
                  {chapter.title.replace(/^Week \d+：/, '')}
                </h3>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 bg-neutral-900 text-neutral-400">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <p>Python 程序设计（Agentic Coding）</p>
          <p className="text-sm mt-2">采用场景驱动 + 贯穿案例 + 循环角色的叙事方式</p>
        </div>
      </footer>
    </div>
  )
}
