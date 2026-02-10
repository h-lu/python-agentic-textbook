'use client'

import * as React from 'react'

interface CleanSidebarProps {
  sections: string[]
}

export function CleanSidebar({ sections }: CleanSidebarProps) {
  const [isCollapsed, setIsCollapsed] = React.useState(false)
  const [activeSection, setActiveSection] = React.useState('')
  const [isVisible, setIsVisible] = React.useState(true)
  const lastScrollY = React.useRef(0)

  // Track scroll direction for auto-hide behavior
  React.useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY
      const scrollDirection = currentScrollY > lastScrollY.current ? 'down' : 'up'

      // Always show when near top, hide when scrolling down past threshold
      if (currentScrollY < 100) {
        setIsVisible(true)
      } else if (scrollDirection === 'down') {
        setIsVisible(false)
      } else {
        setIsVisible(true)
      }

      lastScrollY.current = currentScrollY
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // Track active section on scroll
  React.useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveSection(entry.target.id)
          }
        })
      },
      { threshold: 0.1, rootMargin: '-100px 0px -80% 0px' }
    )

    // Observe all heading elements
    document.querySelectorAll('h2[id^="section-"]').forEach((heading) => {
      observer.observe(heading)
    })

    return () => observer.disconnect()
  }, [sections])

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId)
    if (element) {
      const y = element.getBoundingClientRect().top + window.pageYOffset - 100
      window.scrollTo({ top: y, behavior: 'smooth' })
    }
  }

  return (
    <>
      {/* Mobile sidebar - floating at bottom */}
      <div className="lg:hidden fixed bottom-4 left-4 right-4 z-50">
        <div className="bg-white/95 backdrop-blur-sm border border-slate-200 rounded-xl shadow-lg">
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-slate-700"
          >
            <span>目录</span>
            <svg
              className={`w-4 h-4 transition-transform ${isCollapsed ? '' : 'rotate-180'}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          {!isCollapsed && (
            <nav className="max-h-60 overflow-y-auto border-t border-slate-100">
              <ul className="py-2">
                {sections.map((section, idx) => {
                  const sectionId = `section-${idx}`
                  const isActive = activeSection === sectionId

                  return (
                    <li key={idx}>
                      <a
                        href={`#${sectionId}`}
                        onClick={(e) => {
                          e.preventDefault()
                          scrollToSection(sectionId)
                          setIsCollapsed(true)
                        }}
                        className={`block px-4 py-2 text-sm transition-colors ${
                          isActive
                            ? 'bg-blue-50 text-blue-700 font-medium'
                            : 'text-slate-600 hover:bg-slate-50'
                        }`}
                      >
                        {section}
                      </a>
                    </li>
                  )
                })}
              </ul>
            </nav>
          )}
        </div>
      </div>

      {/* Desktop floating sidebar */}
      <aside
        className={`hidden lg:block fixed left-0 top-0 h-screen z-40 transition-transform duration-300 ${
          isVisible ? 'translate-x-0' : '-translate-x-[calc(100%-12px)]'
        }`}
      >
        <div className="h-full w-72 bg-white/95 backdrop-blur-sm border-r border-slate-200 shadow-sm overflow-hidden">
          <div className="h-full flex flex-col">
            {/* Header */}
            <div className="p-4 border-b border-slate-100">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wide">
                目录
              </h3>
            </div>

            {/* Scrollable content */}
            <nav className="flex-1 overflow-y-auto p-4">
              <ul className="space-y-1">
                {sections.map((section, idx) => {
                  const sectionId = `section-${idx}`
                  const isActive = activeSection === sectionId

                  return (
                    <li key={idx}>
                      <a
                        href={`#${sectionId}`}
                        onClick={(e) => {
                          e.preventDefault()
                          scrollToSection(sectionId)
                        }}
                        className={`block py-2 px-3 rounded-lg text-sm transition-colors ${
                          isActive
                            ? 'bg-blue-50 text-blue-700 font-medium'
                            : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                        }`}
                      >
                        {section}
                      </a>
                    </li>
                  )
                })}
              </ul>
            </nav>
          </div>
        </div>

        {/* Toggle button - visible when sidebar is hidden */}
        <button
          onClick={() => setIsVisible(!isVisible)}
          className={`absolute top-1/2 -translate-y-1/2 bg-white border border-slate-200 shadow-md rounded-r-lg p-2 hover:bg-slate-50 transition-all ${
            isVisible ? 'left-72 opacity-0 pointer-events-none' : 'left-0 opacity-100'
          }`}
          aria-label="展开目录"
        >
          <svg className="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </aside>

      {/* Desktop toggle button when sidebar is visible */}
      <button
        onClick={() => setIsVisible(!isVisible)}
        className={`hidden lg:flex fixed left-72 top-1/2 -translate-y-1/2 z-50 bg-white border border-slate-200 shadow-md rounded-r-lg p-2 hover:bg-slate-50 transition-all duration-300 ${
          isVisible ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        aria-label="收起目录"
      >
        <svg className="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      {/* Spacer for desktop layout - pushes content to the right */}
      <div className={`hidden lg:block transition-all duration-300 ${isVisible ? 'w-72' : 'w-0'}`} />
    </>
  )
}
