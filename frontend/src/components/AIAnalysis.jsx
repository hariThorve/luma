import { useState, useEffect, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import { Clipboard, Check, Sparkles, Zap, Pause, Play } from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import TypewriterEffect from './TypewriterEffect';

function AIAnalysis({ analyses }) {
  const [activeModel, setActiveModel] = useState(Object.keys(analyses)[0]);
  const [copied, setCopied] = useState({});
  const [isTyping, setIsTyping] = useState(true);
  const [typingSpeed, setTypingSpeed] = useState(15); // milliseconds per character
  const [displayedText, setDisplayedText] = useState('');
  
  const currentContent = analyses[activeModel].content;
  
  // Reset typing state when active model changes
  useEffect(() => {
    setIsTyping(true);
    setDisplayedText('');
  }, [activeModel]);
  
  if (!analyses || Object.keys(analyses).length === 0) {
    return (
      <div className="card p-4">
        <p className="text-gray-500">No AI analysis available.</p>
      </div>
    );
  }
  
  const handleCopyCode = (code) => {
    navigator.clipboard.writeText(code);
    setCopied({ [code]: true });
    setTimeout(() => setCopied({}), 2000);
  };
  
  const toggleTyping = () => {
    if (isTyping) {
      // If currently typing, show full text immediately
      setIsTyping(false);
      setDisplayedText(currentContent);
    } else {
      // If paused, restart typing
      setIsTyping(true);
      setDisplayedText('');
    }
  };
  
  // Callback to update the displayed text
  const handleTextUpdate = useCallback((text) => {
    setDisplayedText(text);
    
    // If we've reached the end of the text, stop typing
    if (text.length === currentContent.length) {
      setTimeout(() => setIsTyping(false), 500);
    }
  }, [currentContent]);

  return (
    <div className="card overflow-hidden">
      <div className="border-b border-gray-100">
        <div className="flex overflow-x-auto">
          {Object.keys(analyses).map((modelId) => (
            <button
              key={modelId}
              className={`px-5 py-3 font-medium text-sm whitespace-nowrap flex items-center gap-1.5 ${
                activeModel === modelId
                  ? 'text-indigo-600 bg-indigo-50 relative'
                  : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
              }`}
              onClick={() => setActiveModel(modelId)}
            >
              {activeModel === modelId && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 gradient-bg"></div>
              )}
              {activeModel === modelId ? (
                <Zap size={14} className="text-indigo-500" />
              ) : (
                <Sparkles size={14} className="text-gray-400" />
              )}
              {analyses[modelId].ai_model_id === 'gemini-pro' ? 'Gemini 2.0 Flash' : 'Llama 3 70B'}
            </button>
          ))}
        </div>
      </div>
      
      <div className="p-5 prose max-w-none prose-indigo prose-headings:font-semibold prose-a:text-indigo-600 relative">
        {/* Typing control button */}
        <button 
          onClick={toggleTyping}
          className="absolute top-2 right-2 p-2 rounded-full bg-gray-100 hover:bg-gray-200 z-10"
          title={isTyping ? "Show full text" : "Restart typing animation"}
        >
          {isTyping ? <Pause size={16} /> : <Play size={16} />}
        </button>
        
        {/* Typewriter effect */}
        {isTyping && (
          <TypewriterEffect 
            text={currentContent} 
            speed={typingSpeed} 
            onTextUpdate={handleTextUpdate} 
          />
        )}
        
        {/* Markdown content */}
        <div className="relative">
          <ReactMarkdown
            children={displayedText || currentContent}
            components={{
              code({ node, inline, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || '');
                const code = String(children).replace(/\n$/, '');
                
                if (!inline && match) {
                  return (
                    <div className="relative my-4 rounded-lg overflow-hidden">
                      <div className="bg-gray-800 text-gray-300 text-xs py-1 px-3 flex justify-between items-center">
                        <span>{match[1].toUpperCase()}</span>
                        <button
                          onClick={() => handleCopyCode(code)}
                          className="p-1 rounded hover:bg-gray-700 text-gray-300"
                          title="Copy code"
                        >
                          {copied[code] ? <Check size={14} /> : <Clipboard size={14} />}
                        </button>
                      </div>
                      <SyntaxHighlighter
                        style={vscDarkPlus}
                        language={match[1]}
                        PreTag="div"
                        {...props}
                      >
                        {code}
                      </SyntaxHighlighter>
                    </div>
                  );
                }
                
                return inline ? (
                  <code className="bg-gray-100 px-1 py-0.5 rounded text-red-500 text-sm" {...props}>
                    {children}
                  </code>
                ) : (
                  <div className="relative my-4 bg-gray-900 rounded-lg overflow-hidden">
                    <div className="bg-gray-800 text-gray-300 text-xs py-1 px-3 flex justify-between items-center">
                      <span>CODE</span>
                      <button
                        onClick={() => handleCopyCode(code)}
                        className="p-1 rounded hover:bg-gray-700 text-gray-300"
                        title="Copy code"
                      >
                        {copied[code] ? <Check size={14} /> : <Clipboard size={14} />}
                      </button>
                    </div>
                    <SyntaxHighlighter
                      style={vscDarkPlus}
                      language="text"
                      PreTag="div"
                      {...props}
                    >
                      {code}
                    </SyntaxHighlighter>
                  </div>
                );
              }
            }}
          />
          
          {/* Typing cursor */}
          {isTyping && displayedText && (
            <span className="typing-cursor"></span>
          )}
        </div>
      </div>
    </div>
  );
}

export default AIAnalysis; 