import { Info, Check, Sparkles } from 'lucide-react';
import { useState } from 'react';

function ModelSelector({ availableModels = [], selectedModels = [], setSelectedModels }) {
  const [showInfo, setShowInfo] = useState(null);
  
  const handleModelToggle = (modelId) => {
    if (selectedModels.includes(modelId)) {
      setSelectedModels(selectedModels.filter(id => id !== modelId));
    } else {
      setSelectedModels([...selectedModels, modelId]);
    }
  };
  
  if (!availableModels || availableModels.length === 0) {
    return (
      <div className="text-sm text-gray-500">
        Loading available AI models...
      </div>
    );
  }
  
  return (
    <div className="flex flex-wrap gap-3">
      {availableModels.map((model) => (
        <div key={model.id} className="relative">
          <div 
            className={`
              flex items-center px-4 py-3 rounded-xl border cursor-pointer transition-all
              ${selectedModels.includes(model.id) 
                ? 'bg-indigo-50 border-indigo-200 text-indigo-800 shadow-sm' 
                : 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50'}
            `}
            onClick={() => handleModelToggle(model.id)}
          >
            <div className={`
              w-5 h-5 rounded-full mr-3 flex items-center justify-center
              ${selectedModels.includes(model.id) 
                ? 'gradient-bg text-white' 
                : 'border border-gray-300'}
            `}>
              {selectedModels.includes(model.id) && <Check size={12} />}
            </div>
            <span className="font-medium">{model.name}</span>
            <Sparkles size={14} className="ml-1.5 text-indigo-400" />
            <button
              type="button"
              className="ml-2 text-gray-400 hover:text-gray-600 p-1"
              onClick={(e) => {
                e.stopPropagation();
                setShowInfo(showInfo === model.id ? null : model.id);
              }}
              aria-label="Model information"
            >
              <Info size={16} />
            </button>
          </div>
          
          {showInfo === model.id && (
            <div className="absolute z-10 mt-2 w-72 bg-white border border-gray-100 rounded-xl shadow-lg p-4 text-sm glass">
              <p className="font-medium gradient-text">{model.name}</p>
              <p className="text-gray-500 text-xs mt-1">Provider: {model.provider}</p>
              <p className="mt-2 text-gray-700">{model.description}</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default ModelSelector; 