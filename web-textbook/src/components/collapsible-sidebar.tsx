'use client'

import * as React from 'react'

interface CollapsibleSidebarProps {
  sections: string[]
  children?: React.ReactNode
}

export function CollapsibleSidebar({ sections }: CollapsibleSidebarProps) {
  const [isOpen, setIsOpen] = React.useState(true)

  return (
    <>
      {/* Toggle button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed bottom-4 left-4 z-50 bg-primary-500 text-white p-3 rounded-full shadow-lg hover:bg-primary-600 transition-colors"
        aria-label={isOpen ? '隐藏目录' : '显示目录'}
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          {isOpen ? (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
          )}
        </svg>
      </button>

      {/* Desktop collapse button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="hidden lg:flex fixed left-0 top-1/2 -translate-y-1/2 z-40 bg-white border border-neutral-200 rounded-r-lg shadow-md p-2 hover:bg-neutral-50 transition-all"
        style={{ left: isOpen ? '30%' : '0' }}
        aria-label={isOpen ? '折叠目录' : '展开目录'}
      >
        <svg className="w-5 h-5 text-neutral-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          {isOpen ? (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
          )}
        </svg>
      </button>

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:sticky top-0 left-0 h-screen lg:h-auto bg-white border-r border-neutral-200
          overflow-y-auto z-30 transition-all duration-300 ease-in-out
          ${isOpen ? 'w-[80%] lg:w-[30%]' : 'w-0 lg:w-0'}
        `}
      >
        {isOpen && (
          <div className="p-6">
            <h3 className="text-lg font-semibold text-neutral-900 mb-4">本节目录</h3>
            <nav>
              <ul className="space-y-2">
                {sections.map((section, idx) => (
                  <li key={idx}>
                    <a
                      href={`#section-${idx}`}
                      className="block py-2 px-3 rounded-lg text-neutral-600 hover:text-primary-600 hover:bg-primary-50 transition-colors"
                      onClick={() => {
                        // Close mobile menu after clicking
                        if (window.innerWidth < 1024) setIsOpen(false)
                      }}
                    >
                      {section}
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
          className="fixed inset-0 bg-black/50 z-20 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  )
}
