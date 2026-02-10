'use client'

import * as React from 'react'
import { codeBlockTheme } from '@/lib/design-system'

interface CollapsibleCodeProps {
  code: string
  language?: string
  filename?: string
  defaultOpen?: boolean
}

export function CollapsibleCode({
  code,
  language = 'python',
  filename = 'python',
  defaultOpen = true,
}: CollapsibleCodeProps) {
  const [isOpen, setIsOpen] = React.useState(defaultOpen)
  const [copied, setCopied] = React.useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="my-6 rounded-lg overflow-hidden border border-neutral-300">
      {/* Header */}
      <div className="flex items-center justify-between bg-neutral-100 px-4 py-2 border-b border-neutral-300">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="flex items-center gap-2 text-sm font-medium text-neutral-700 hover:text-neutral-900 transition-colors"
          >
            <svg
              className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-90' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
            <span className="font-mono text-sm bg-neutral-200 px-2 py-0.5 rounded">
              {filename}
            </span>
          </button>
        </div>
        <button
          onClick={handleCopy}
          className="text-sm text-neutral-600 hover:text-neutral-900 transition-colors flex items-center gap-1"
        >
          {copied ? (
            <>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              已复制
            </>
          ) : (
            <>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              复制
            </>
          )}
        </button>
      </div>

      {/* Code content */}
      {isOpen && (
        <div className="bg-neutral-900 overflow-x-auto custom-scrollbar">
          <pre className="p-4 m-0">
            <code className={`language-${language} text-sm text-neutral-100`}>{code}</code>
          </pre>
        </div>
      )}
    </div>
  )
}
