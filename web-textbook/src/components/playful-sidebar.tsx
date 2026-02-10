'use client'

import * as React from 'react'

interface PlayfulSidebarProps {
  sections: string[]
}

export function PlayfulSidebar({ sections }: PlayfulSidebarProps) {
  const [isOpen, setIsOpen] = React.useState(true)

  return (
    <>
      {/* Mobile toggle - playful floating button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed bottom-6 left-4 z-50 bg-gradient-to-r from-indigo-500 to-purple-500 text-white p-3 rounded-full shadow-lg hover:shadow-xl transition-all hover:scale-110"
        aria-label={isOpen ? '隐藏目录' : '显示目录'}
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          {isOpen ? (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          )}
        </svg>
      </button>

      {/* Desktop collapse button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="hidden lg:flex fixed left-0 top-1/2 -translate-y-1/2 z-40 bg-white border-2 border-indigo-200 rounded-r-xl shadow-md p-2 hover:bg-indigo-50 hover:border-indigo-300 transition-all"
        style={{ left: isOpen ? '30%' : '0' }}
        aria-label={isOpen ? '折叠目录' : '展开目录'}
      >
        <svg className="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          {isOpen ? (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M15 19l-7-7 7-7" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5l7 7-7 7" />
          )}
        </svg>
      </button>

      {/* Sidebar - playful gradient background */}
      <aside
        className={`
          fixed lg:sticky top-0 left-0 h-screen lg:h-auto overflow-y-auto z-30 transition-all duration-300 ease-out
          ${isOpen ? 'w-[80%] lg:w-[30%]' : 'w-0'}
        `}
      >
        {isOpen && (
          <div className="p-6 bg-gradient-to-b from-indigo-50 to-purple-50 min-h-full lg:min-h-0">
            <div className="mb-6">
              <h3 className="text-xl font-bold text-indigo-900 flex items-center gap-2">
                <span className="text-2xl">📚</span>
                本节目录
              </h3>
              <p className="text-sm text-indigo-600/70 mt-1">点击跳转到对应内容</p>
            </div>
            <nav>
              <ul className="space-y-1">
                {sections.map((section, idx) => (
                  <li key={idx}>
                    <a
                      href={`#section-${idx}`}
                      className="flex items-center gap-3 py-3 px-4 rounded-xl text-slate-700 hover:text-indigo-700 hover:bg-white hover:shadow-md transition-all group"
                      onClick={() => {
                        if (window.innerWidth < 1024) setIsOpen(false)
                      }}
                    >
                      <span className="flex-shrink-0 w-7 h-7 rounded-full bg-indigo-100 text-indigo-600 text-sm font-bold flex items-center justify-center group-hover:bg-indigo-500 group-hover:text-white transition-colors">
                        {idx + 1}
                      </span>
                      <span className="font-medium">{section}</span>
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          </div>
        )}
      </aside>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-indigo-900/30 backdrop-blur-sm z-20 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  )
}
