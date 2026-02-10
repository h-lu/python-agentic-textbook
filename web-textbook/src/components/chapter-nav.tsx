'use client'

import * as React from 'react'

interface ChapterNavProps {
  sections: string[]
  activeSection?: string
}

export function ChapterNav({ sections, activeSection }: ChapterNavProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false)

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        className="lg:hidden fixed bottom-4 right-4 z-50 bg-primary-500 text-white p-3 rounded-full shadow-lg"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      {/* Sidebar */}
      <aside className={`
        fixed lg:sticky top-0 left-0 h-screen lg:h-auto w-72 bg-white border-r border-neutral-200
        overflow-y-auto z-40 transition-transform duration-300
        ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="p-6">
          <h3 className="text-lg font-semibold text-neutral-900 mb-4">本节目录</h3>
          <nav>
            <ul className="space-y-2">
              {sections.map((section, index) => (
                <li key={index}>
                  <a
                    href={`#section-${index}`}
                    className={`
                      block py-2 px-3 rounded-lg text-sm transition-colors
                      ${activeSection === section
                        ? 'bg-primary-100 text-primary-700 font-medium'
                        : 'text-neutral-600 hover:bg-neutral-100 hover:text-neutral-900'
                      }
                    `}
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    {section}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </aside>

      {/* Overlay for mobile */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </>
  )
}
