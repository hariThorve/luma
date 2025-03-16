import { useEffect, useRef } from 'react';

function TypewriterEffect({ text, speed = 10, onTextUpdate = () => {} }) {
  const timeoutRef = useRef(null);
  const currentIndexRef = useRef(0);
  
  useEffect(() => {
    // Reset when text changes
    currentIndexRef.current = 0;
    onTextUpdate(''); // Start with empty text
    
    // Clear any existing timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    
    // Function to type the next character
    const typeNextChar = () => {
      // Check if we still have characters to type
      if (currentIndexRef.current < text.length) {
        // Get the text up to the current index
        const newText = text.substring(0, currentIndexRef.current + 1);
        // Update the displayed text
        onTextUpdate(newText);
        // Move to the next character
        currentIndexRef.current += 1;
        
        // Calculate the delay for the next character
        let nextDelay = speed;
        
        // If we have more characters to type
        if (currentIndexRef.current < text.length) {
          const nextChar = text[currentIndexRef.current];
          // Type faster for spaces and punctuation
          if (nextChar === ' ' || [',', '.', '!', '?', '\n'].includes(nextChar)) {
            nextDelay = Math.max(speed / 2, 1);
          }
        }
        
        // Schedule the next character
        timeoutRef.current = setTimeout(typeNextChar, nextDelay);
      }
    };
    
    // Start typing after a short delay
    timeoutRef.current = setTimeout(typeNextChar, 300);
    
    // Cleanup function
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [text, speed, onTextUpdate]);

  return null; // This component doesn't render anything
}

export default TypewriterEffect; 