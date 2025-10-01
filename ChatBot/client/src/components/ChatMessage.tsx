import { Bot, User } from 'lucide-react';
import { Message } from '../types/chat';

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-3 p-4 ${isUser ? 'bg-white' : 'bg-slate-50'}`}>
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isUser ? 'bg-blue-600' : 'bg-emerald-600'
      }`}>
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>
      <div className="flex-1 space-y-1">
        <div className="font-medium text-sm text-slate-900">
          {isUser ? 'You' : 'Alpha Bot'}
        </div>
        <div className="text-slate-700 leading-relaxed whitespace-pre-wrap">
          {message.content}
        </div>
        <div className="text-xs text-slate-400">
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}
