import { Bot, Settings } from 'lucide-react';

interface ChatHeaderProps {
  onSettingsClick: () => void;
}

export default function ChatHeader({ onSettingsClick }: ChatHeaderProps) {
  return (
    <div className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white p-4 shadow-md">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-white/20 backdrop-blur-sm p-2 rounded-lg">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold">Alpha Bot</h1>
            <p className="text-sm text-emerald-50">AI Assistant</p>
          </div>
        </div>
        <button
          onClick={onSettingsClick}
          className="p-2 hover:bg-white/20 rounded-lg transition-colors"
          aria-label="Settings"
        >
          <Settings className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
