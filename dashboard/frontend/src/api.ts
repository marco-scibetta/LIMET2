async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(path, init)
  if (!r.ok) {
    const t = await r.text().catch(() => '')
    throw new Error(`${r.status} ${r.statusText}${t ? `: ${t}` : ''}`)
  }
  return r.json() as Promise<T>
}

export const get = <T>(path: string) => req<T>(path)

export const post = <T>(path: string, body?: unknown) =>
  req<T>(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
  })
