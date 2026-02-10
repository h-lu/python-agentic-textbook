'use client'

import * as React from 'react'

interface SimpleCodeBlockProps {
  code: string
  language?: string
  filename?: string
}

export function SimpleCodeBlock({
  code,
  language = 'python',
  filename = 'python',
}: SimpleCodeBlockProps) {
  const [copied, setCopied] = React.useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="my-5 rounded-xl overflow-hidden border border-indigo-100 bg-gradient-to-br from-slate-900 to-slate-800 shadow-lg">
      {/* Header - minimal */}
      <div className="flex items-center justify-between px-4 py-2 bg-slate-800/50 border-b border-slate-700/50">
        <span className="text-xs font-medium text-indigo-300 font-mono">{filename}</span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition-colors group"
        >
          {copied ? (
            <>
              <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              <span className="text-green-400">已复制</span>
            </>
          ) : (
            <>
              <svg className="w-4 h-4 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <span>复制</span>
            </>
          )}
        </button>
      </div>

      {/* Code content - always visible */}
      <pre className="p-4 m-0 overflow-x-auto">
        <code className={`language-${language} text-sm leading-relaxed`}>{code}</code>
      </pre>
    </div>
  )
}
