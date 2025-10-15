import React, { useEffect, useRef } from 'react';

// Declare DeepChat custom element for TypeScript
declare global {
  namespace JSX {
    interface IntrinsicElements {
      'deep-chat': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement> & {
        ref?: React.Ref<DeepChatElement>;
        style?: React.CSSProperties;
      };
    }
  }
}

interface DeepChatElement extends HTMLElement {
  request?: {
    url: string;
    method: string;
    headers: Record<string, string>;
  };
  initialMessages?: Array<{
    role: string;
    text: string;
  }>;
  textInput?: {
    placeholder?: {
      text: string;
    };
    styles?: {
      container?: Record<string, string>;
    };
  };
  messageStyles?: {
    default?: {
      shared?: {
        bubble?: Record<string, string>;
      };
      user?: {
        bubble?: Record<string, string>;
      };
      ai?: {
        bubble?: Record<string, string>;
      };
    };
  };
}

const App: React.FC = () => {
  const chatRef = useRef<DeepChatElement>(null);

  useEffect(() => {
    if (chatRef.current) {
      // Configure DeepChat
      chatRef.current.request = {
        url: "http://localhost:45667/incoming_message",
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        }
      };

      // Optional: Add initial messages
      chatRef.current.initialMessages = [
        {
          role: "ai",
          text: "你好，我可以帮你查询虚拟币的最新交易价格~"
        }
      ];

      // Use setAttribute for style as it's inherited from HTMLElement
      chatRef.current.setAttribute('style', 
        'border-radius: 10px; border: 1px solid #e5e7eb; font-family: system-ui, -apple-system, sans-serif;'
      );

      chatRef.current.textInput = {
        placeholder: {
          text: "Type your message here..."
        },
        styles: {
          container: {
            borderRadius: "20px",
            border: "1px solid #d1d5db",
            padding: "10px"
          }
        }
      };

      chatRef.current.messageStyles = {
        default: {
          shared: {
            bubble: {
              maxWidth: "70%",
              padding: "12px 16px",
              borderRadius: "18px",
              fontSize: "15px"
            }
          },
          user: {
            bubble: {
              backgroundColor: "#2563eb",
              color: "white"
            }
          },
          ai: {
            bubble: {
              backgroundColor: "#f3f4f6",
              color: "#1f2937"
            }
          }
        }
      };
    }
  }, []);

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      display: 'flex',
      flexDirection: 'column',
      backgroundColor: '#f9fafb'
    }}>
      <header style={{
        backgroundColor: 'white',
        padding: '20px',
        borderBottom: '1px solid #e5e7eb',
        boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
      }}>
        <h1 style={{
          margin: 0,
          fontSize: '24px',
          fontWeight: '600',
          color: '#1f2937'
        }}>
          DeepChat Bot
        </h1>
        <p style={{
          margin: '4px 0 0 0',
          fontSize: '14px',
          color: '#6b7280'
        }}>
          Powered by DeepChat & FastAPI
        </p>
      </header>
      
      <div style={{
        flex: 1,
        padding: '20px',
        display: 'flex',
        justifyContent: 'center',
        overflow: 'hidden'
      }}>
        <div style={{
          width: '100%',
          maxWidth: '900px',
          height: '100%'
        }}>
          <deep-chat
            ref={chatRef}
            style={{
              width: '100%',
              height: '100%'
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
