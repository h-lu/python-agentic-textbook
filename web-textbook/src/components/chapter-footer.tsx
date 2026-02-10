import Link from 'next/link'

interface ChapterFooterProps {
  prevChapter?: { week: string; title: string }
  nextChapter?: { week: string; title: string }
}

export function ChapterFooter({ prevChapter, nextChapter }: ChapterFooterProps) {
  return (
    <footer className="mt-16 pt-8 border-t border-slate-200">
      <nav className="flex justify-between items-start gap-4">
        {prevChapter ? (
          <Link
            href={`/week-${prevChapter.week}`}
            className="flex-1 p-4 rounded-lg border border-slate-200 hover:border-blue-300 hover:bg-slate-50 transition-colors"
          >
            <div className="text-xs font-medium text-slate-500 mb-1">← 上一章</div>
            <div className="font-medium text-slate-700 line-clamp-2">
              {prevChapter.title.replace(/^Week \d+：/, '')}
            </div>
          </Link>
        ) : (
          <div className="flex-1" />
        )}

        {nextChapter ? (
          <Link
            href={`/week-${nextChapter.week}`}
            className="flex-1 p-4 rounded-lg border border-slate-200 hover:border-blue-300 hover:bg-slate-50 transition-colors text-right"
          >
            <div className="text-xs font-medium text-slate-500 mb-1">下一章 →</div>
            <div className="font-medium text-slate-700 line-clamp-2">
              {nextChapter.title.replace(/^Week \d+：/, '')}
            </div>
          </Link>
        ) : (
          <div className="flex-1" />
        )}
      </nav>

      <div className="text-center mt-8">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-sm text-slate-500 hover:text-slate-700 transition-colors"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          返回首页
        </Link>
      </div>
    </footer>
  )
}
