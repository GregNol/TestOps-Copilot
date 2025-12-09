import { createHighlighter } from 'shiki'
import MarkdownIt from 'markdown-it'

let highlighter: any = null
const md = new MarkdownIt({ html: true, linkify: true, typographer: true, breaks: true })

export async function initializeHighlighter() {
  if (!highlighter) {
    highlighter = await createHighlighter({ 
      themes: ['light-plus', 'dark-plus'], 
      langs: ['javascript','typescript','python','java','cpp','c','csharp','go','rust','ruby','php','swift','kotlin','sql','html','css','json','xml','yaml','bash','shell','zsh','powershell','dockerfile','makefile','markdown'] 
    })
  }
  return highlighter
}

export async function renderMarkdown(content: string): Promise<string> {
  const hl = await initializeHighlighter()
  const defaultFence = md.renderer.rules.fence!

  md.renderer.rules.fence = (tokens, idx) => {
    const token = tokens[idx]
    const info = token.info ? token.info.trim() : ''
    const langName = info.split(/\s+/g)[0]
    const code = token.content
    if (!langName) return `<pre><code>${md.utils.escapeHtml(code)}</code></pre>`
    try {
      const isDark = document.documentElement.classList.contains('dark')
      const theme = isDark ? 'dark-plus' : 'light-plus'
      const html = hl.codeToHtml(code, { lang: langName, theme })
      return html
    } catch (e) {
      return `<pre><code class="language-${langName}">${md.utils.escapeHtml(code)}</code></pre>`
    }
  }

  return md.render(content)
}

export async function renderMarkdownInline(content: string): Promise<string> { return md.renderInline(content) }
