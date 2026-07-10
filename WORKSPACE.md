# Workspace Info (auto-generated, do not edit)

## Workspace: 잡다

- **분석 Chat** (project: 분석, dir: D:\claude\result) — mode: confirm
- **Nblog Chat** (project: Nblog, dir: D:\claude\Nblog) — mode: confirm
- **플리퍼 전자책 Chat** (project: 플리퍼 전자책, dir: D:\claude\fbook) — mode: confirm
- **freetv Chat** [freeTV] (project: freetv, dir: D:\claude\freetv) — mode: confirm
- **thai-semantle Chat** (project: thai-semantle, dir: D:\claude\thai-semantle) — mode: confirm

## Shared Directory
A `shared/` directory is available in your project root for cross-project file exchange.

Rules:
- Write files to `shared/` when other projects need them
- After writing files to `shared/`, ALWAYS notify other projects using `__notify__`
- When you receive a shared file notification, check `shared/` for new files
- Do NOT modify or delete files created by other projects unless instructed

## How to notify a related bot
Include this JSON in your response:
```json
{"__notify__": {"target": "bot_name_here", "message": "description of changes"}}
```
The bot system will route your message to the target bot's Claude session.

## How to ask a related bot a question
Include this JSON in your response to ask another bot and wait for their answer:
```json
{"__ask__": {"target": "bot_name_here", "question": "your question here"}}
```
The bot system will send your question to the target bot, wait for their answer, and feed it back to you.

## How to create a TODO task for a related bot
Include this JSON in your response to assign a task to another bot:
```json
{"__todo__": {"target": "bot_name_here", "title": "task title", "description": "detailed description"}}
```
The bot system will create a TODO task and notify the target bot.

## How to mark a TODO task as completed
After completing a task from your TODO.md, include this in your response:
```json
{"__todo_done__": {"id": "task-uuid-from-TODO.md", "result": "what you did"}}
```
