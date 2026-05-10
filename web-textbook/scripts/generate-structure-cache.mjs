#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const chaptersDir = path.join(root, 'public', 'chapters')
const outputPath = path.join(root, '.structure-cache.json')

function readMarkdown(file) {
  return fs.readFileSync(file, 'utf8')
}

function extractTitle(content, fallback) {
  const match = content.match(/^#\s+(.+)$/m)
  return match ? match[1].trim() : fallback
}

function extractSections(content) {
  return [...content.matchAll(/^##\s+(.+)$/gm)].map(match => match[1].trim())
}

function countCodeBlocks(content) {
  return (content.match(/```/g) || []).length / 2 | 0
}

function stageForWeek(week) {
  const n = Number(week)
  if (n <= 5) return '入门基础'
  if (n <= 10) return '工程进阶'
  return '综合实战'
}

if (!fs.existsSync(chaptersDir)) {
  console.error(`[structure-cache] missing chapters dir: ${chaptersDir}`)
  process.exit(1)
}

const files = fs.readdirSync(chaptersDir)
  .filter(name => /^week-\d{2}\.md$/.test(name))
  .sort()

if (files.length === 0) {
  console.error('[structure-cache] no public/chapters/week-XX.md files found')
  process.exit(1)
}

const chapters = files.map(file => {
  const week = file.match(/week-(\d{2})\.md/)[1]
  const fullPath = path.join(chaptersDir, file)
  const content = readMarkdown(fullPath)
  return {
    week,
    title: extractTitle(content, `Week ${week}`),
    file: `chapters/${file}`,
    sections: extractSections(content),
    code_blocks: countCodeBlocks(content),
  }
})

const stageMap = new Map()
for (const chapter of chapters) {
  const stage = stageForWeek(chapter.week)
  if (!stageMap.has(stage)) stageMap.set(stage, [])
  stageMap.get(stage).push(chapter.week)
}

const data = {
  syllabus: {
    title: 'Python 程序设计（Agentic Coding）',
    stages: [...stageMap.entries()].map(([name, weeks]) => ({ name, weeks })),
  },
  chapters,
  generated_at: new Date().toISOString(),
}

fs.writeFileSync(outputPath, `${JSON.stringify(data, null, 2)}\n`, 'utf8')
console.log(`[structure-cache] wrote ${path.relative(root, outputPath)} (${chapters.length} chapters)`)
