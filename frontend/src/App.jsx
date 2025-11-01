// import { useState, useRef, useEffect } from "react";

// function App() {
//   // Configuration
//   const config = {
//     apiEndpoint: "http://localhost:8000/chat",
//     acceptedFiles: ".pdf,.doc,.docx,.txt",
//   };

//   // Translations (unchanged)
//   const translations = {
//     en: {
//       title: "Assistant CV",
//       placeholder: "Message Assistant CV...",
//       newChat: "New Chat",
//       clearChat: "Clear Chat",
//       darkMode: "Dark Mode",
//       language: "Language",
//       exportChat: "Export Chat",
//       menu: "Menu",
//       send: "Send",
//       uploading: "Uploading...",
//       error: "Error occurred",
//       history: "Chat History",
//     },
//     fr: {
//       title: "Assistant CV",
//       placeholder: "Message Assistant CV...",
//       newChat: "Nouvelle Discussion",
//       clearChat: "Effacer Discussion",
//       darkMode: "Mode Sombre",
//       language: "Langue",
//       exportChat: "Exporter Discussion",
//       menu: "Menu",
//       send: "Envoyer",
//       uploading: "Téléchargement...",
//       error: "Erreur survenue",
//       history: "Historique des discussions",
//     },
//     ar: {
//       title: "مساعد السيرة الذاتية",
//       placeholder: "...اكتب رسالة",
//       newChat: "محادثة جديدة",
//       clearChat: "مسح المحادثة",
//       darkMode: "الوضع الداكن",
//       language: "اللغة",
//       exportChat: "تصدير المحادثة",
//       menu: "القائمة",
//       send: "إرسال",
//       uploading: "...جاري الرفع",
//       error: "حدث خطأ",
//       history: "سجل المحادثات",
//     },
//   };

//   // State
//   const [messages, setMessages] = useState([
//     { role: "assistant", content: "Hello! How can I help you today?" },
//   ]);
//   const [conversations, setConversations] = useState([]);
//   const [currentConversationId, setCurrentConversationId] = useState(Date.now());
//   const [input, setInput] = useState("");
//   const [uploadFile, setUploadFile] = useState(null);
//   const [isLoading, setIsLoading] = useState(false);
//   const [darkMode, setDarkMode] = useState(false);
//   const [language, setLanguage] = useState("en");
//   const [menuOpen, setMenuOpen] = useState(false);

//   const fileInputRef = useRef(null);
//   const messagesEndRef = useRef(null);
//   const textareaRef = useRef(null);

//   const t = translations[language];
//   const isRTL = language === "ar";

//   const scrollToBottom = () => {
//     messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   };

//   useEffect(() => {
//     scrollToBottom();
//   }, [messages]);

//   useEffect(() => {
//     if (textareaRef.current) {
//       textareaRef.current.style.height = "auto";
//       textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + "px";
//     }
//   }, [input]);

//   const saveCurrentConversation = () => {
//     setConversations((prev) => {
//       const updatedConversations = prev.filter(
//         (conv) => conv.id !== currentConversationId
//       );
//       return [
//         ...updatedConversations,
//         { id: currentConversationId, messages, timestamp: new Date().toISOString() },
//       ];
//     });
//   };

//   const startNewChat = () => {
//     if (messages.length > 1) {
//       saveCurrentConversation();
//     }
//     const newConversationId = Date.now();
//     setMessages([{ role: "assistant", content: "Hello! How can I help you today?" }]);
//     setCurrentConversationId(newConversationId);
//     setMenuOpen(false);
//   };

//   const loadConversation = (conversationId) => {
//     const conversation = conversations.find((conv) => conv.id === conversationId);
//     if (conversation) {
//       setMessages(conversation.messages);
//       setCurrentConversationId(conversationId);
//       setMenuOpen(false);
//     }
//   };

//   const sendMessage = async () => {
//     if (!input.trim() && !uploadFile) return;

//     const userMessage = input.trim();
//     const newMessages = [...messages];

//     if (userMessage) {
//       newMessages.push({ role: "user", content: userMessage });
//     }
//     if (uploadFile) {
//       newMessages.push({ role: "user", content: `📎 ${uploadFile.name}` });
//     }

//     setMessages(newMessages);
//     setInput("");
//     const currentFile = uploadFile;
//     setUploadFile(null);
//     if (fileInputRef.current) fileInputRef.current.value = "";
//     setIsLoading(true);

//     try {
//       const formData = new FormData();
//       formData.append("message", userMessage);
//       formData.append("format_type", "clean");
//       if (currentFile) {
//         formData.append("file", currentFile);
//       }

//       const response = await fetch(config.apiEndpoint, {
//         method: "POST",
//         body: formData,
//       });

//       if (!response.ok) throw new Error("Network response was not ok");

//       const data = await response.json();
//       setMessages((prev) => [
//         ...prev,
//         { role: "assistant", content: data.reply || data.response || data.message },
//       ]);
//     } catch (error) {
//       console.error("Error:", error);
//       setMessages((prev) => [
//         ...prev,
//         { role: "assistant", content: `${t.error}: ${error.message}` },
//       ]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleKeyDown = (e) => {
//     if (e.key === "Enter" && !e.shiftKey) {
//       e.preventDefault();
//       sendMessage();
//     }
//   };

//   const clearChat = () => {
//     setMessages([]);
//     setMenuOpen(false);
//   };

//   const exportChat = () => {
//     const chatText = messages.map((msg) => 
//       `${msg.role === "user" ? "User" : "Assistant"}: ${msg.content}`
//     ).join("\n\n");
    
//     const blob = new Blob([chatText], { type: "text/plain" });
//     const url = URL.createObjectURL(blob);
//     const a = document.createElement("a");
//     a.href = url;
//     a.download = `chat-export-${new Date().toISOString().slice(0, 10)}.txt`;
//     document.body.appendChild(a);
//     a.click();
//     document.body.removeChild(a);
//     URL.revokeObjectURL(url);
//     setMenuOpen(false);
//   };

//   const theme = {
//     bg: darkMode ? "#212121" : "#ffffff",
//     bgAlt: darkMode ? "#2f2f2f" : "#f7f7f8",
//     text: darkMode ? "#ececec" : "#374151",
//     textLight: darkMode ? "#b4b4b4" : "#6b7280",
//     border: darkMode ? "#444" : "#e5e7eb",
//     headerBg: darkMode ? "#1a1a1a" : "#ffffff",
//     buttonBg: darkMode ? "#3a3a3a" : "#f3f4f6",
//     buttonHover: darkMode ? "#4a4a4a" : "#e5e7eb",
//     accent: darkMode ? "#10a37f" : "#10a37f",
//   };

//   return (
//     <div
//       style={{
//         display: "flex",
//         height: "100vh",
//         width: "100vw",
//         fontFamily: "system-ui, -apple-system, sans-serif",
//         backgroundColor: theme.bg,
//         color: theme.text,
//         overflow: "hidden",
//         direction: isRTL ? "rtl" : "ltr",
//       }}
//     >
//       {/* Sidebar Menu */}
//       <div
//         style={{
//           width: menuOpen ? "260px" : "0",
//           backgroundColor: theme.headerBg,
//           borderRight: `1px solid ${theme.border}`,
//           transition: "width 0.3s",
//           overflow: "hidden",
//           display: "flex",
//           flexDirection: "column",
//         }}
//       >
//         <div style={{ padding: "20px" }}>
//           <button
//             onClick={startNewChat}
//             style={{
//               width: "100%",
//               padding: "12px",
//               backgroundColor: theme.buttonBg,
//               border: "none",
//               borderRadius: "8px",
//               cursor: "pointer",
//               fontSize: "14px",
//               fontWeight: "500",
//               color: theme.text,
//               marginBottom: "10px",
//             }}
//           >
//             ✨ {t.newChat}
//           </button>

//           <button
//             onClick={clearChat}
//             style={{
//               width: "100%",
//               padding: "12px",
//               backgroundColor: theme.buttonBg,
//               border: "none",
//               borderRadius: "8px",
//               cursor: "pointer",
//               fontSize: "14px",
//               color: theme.text,
//               marginBottom: "20px",
//             }}
//           >
//             🗑️ {t.clearChat}
//           </button>

//           {/* Conversation History */}
//           <div style={{ marginBottom: "20px" }}>
//             <h3 style={{ fontSize: "14px", margin: "0 0 10px" }}>{t.history}</h3>
//             {conversations.length === 0 ? (
//               <p style={{ fontSize: "12px", color: theme.textLight }}>
//                 No previous conversations
//               </p>
//             ) : (
//               conversations.map((conv) => (
//                 <button
//                   key={conv.id}
//                   onClick={() => loadConversation(conv.id)}
//                   style={{
//                     width: "100%",
//                     padding: "10px",
//                     backgroundColor:
//                       conv.id === currentConversationId ? theme.accent : theme.buttonBg,
//                     border: "none",
//                     borderRadius: "6px",
//                     cursor: "pointer",
//                     fontSize: "12px",
//                     color: conv.id === currentConversationId ? "white" : theme.text,
//                     marginBottom: "5px",
//                     textAlign: isRTL ? "right" : "left",
//                     overflow: "hidden",
//                     textOverflow: "ellipsis",
//                     whiteSpace: "nowrap",
//                   }}
//                 >
//                   {conv.messages[0]?.content.substring(0, 30) || `Chat ${conv.id}`}
//                 </button>
//               ))
//             )}
//           </div>

//           <div
//             style={{
//               borderTop: `1px solid ${theme.border}`,
//               paddingTop: "20px",
//             }}
//           >
//             <div style={{ marginBottom: "15px" }}>
//               <label
//                 style={{
//                   display: "flex",
//                   alignItems: "center",
//                   gap: "10px",
//                   cursor: "pointer",
//                   fontSize: "14px",
//                 }}
//               >
//                 <input
//                   type="checkbox"
//                   checked={darkMode}
//                   onChange={(e) => setDarkMode(e.target.checked)}
//                   style={{ width: "18px", height: "18px", cursor: "pointer" }}
//                 />
//                 🌙 {t.darkMode}
//               </label>
//             </div>

//             <div style={{ marginBottom: "15px" }}>
//               <label
//                 style={{
//                   fontSize: "14px",
//                   display: "block",
//                   marginBottom: "8px",
//                 }}
//               >
//                 🌐 {t.language}
//               </label>
//               <select
//                 value={language}
//                 onChange={(e) => setLanguage(e.target.value)}
//                 style={{
//                   width: "100%",
//                   padding: "8px",
//                   backgroundColor: theme.buttonBg,
//                   border: `1px solid ${theme.border}`,
//                   borderRadius: "6px",
//                   color: theme.text,
//                   cursor: "pointer",
//                   fontSize: "14px",
//                 }}
//               >
//                 <option value="en">English</option>
//                 <option value="fr">Français</option>
//                 <option value="ar">العربية</option>
//               </select>
//             </div>

//             <button
//               onClick={exportChat}
//               style={{
//                 width: "100%",
//                 padding: "12px",
//                 backgroundColor: theme.buttonBg,
//                 border: "none",
//                 borderRadius: "8px",
//                 cursor: "pointer",
//                 fontSize: "14px",
//                 color: theme.text,
//               }}
//             >
//               💾 {t.exportChat}
//             </button>
//           </div>
//         </div>
//       </div>

//       {/* Main Chat Area (unchanged from original) */}
//       <div
//         style={{
//           flex: 1,
//           display: "flex",
//           flexDirection: "column",
//           overflow: "hidden",
//         }}
//       >
//         {/* Header */}
//         <div
//           style={{
//             borderBottom: `1px solid ${theme.border}`,
//             padding: "14px 20px",
//             backgroundColor: theme.headerBg,
//             display: "flex",
//             alignItems: "center",
//             gap: "15px",
//           }}
//         >
//           <button
//             onClick={() => setMenuOpen(!menuOpen)}
//             style={{
//               padding: "8px 12px",
//               backgroundColor: "transparent",
//               border: "none",
//               cursor: "pointer",
//               fontSize: "20px",
//               color: theme.text,
//             }}
//           >
//             ☰
//           </button>
//           <h1
//             style={{
//               margin: 0,
//               fontSize: "18px",
//               fontWeight: "600",
//               color: theme.text,
//             }}
//           >
//             {t.title}
//           </h1>
//         </div>

//         {/* Messages Container */}
//         <div
//           style={{
//             flex: 1,
//             overflowY: "auto",
//             backgroundColor: theme.bg,
//           }}
//         >
//           <div style={{ width: "100%" }}>
//             {messages.map((msg, idx) => (
//               <div
//                 key={idx}
//                 style={{
//                   padding: "28px 24px",
//                   backgroundColor: msg.role === "assistant" ? theme.bgAlt : theme.bg,
//                   borderBottom: `1px solid ${theme.border}`,
//                   width: "100%",
//                   boxSizing: "border-box",
//                 }}
//               >
//                 <div
//                   style={{
//                     display: "flex",
//                     gap: "20px",
//                     maxWidth: "900px",
//                     margin: "0 auto",
//                     flexDirection: isRTL ? "row-reverse" : "row",
//                   }}
//                 >
//                   <div
//                     style={{
//                       width: "36px",
//                       height: "36px",
//                       borderRadius: "6px",
//                       display: "flex",
//                       alignItems: "center",
//                       justifyContent: "center",
//                       flexShrink: 0,
//                       backgroundColor: msg.role === "assistant" ? theme.accent : "#5436da",
//                       color: "white",
//                       fontSize: "14px",
//                       fontWeight: "600",
//                     }}
//                   >
//                     {msg.role === "assistant" ? "AI" : "U"}
//                   </div>
//                   <div
//                     style={{
//                       flex: 1,
//                       paddingTop: "6px",
//                       minWidth: 0,
//                     }}
//                   >
//                     <p
//                       style={{
//                         margin: 0,
//                         lineHeight: "1.75",
//                         color: theme.text,
//                         fontSize: "15px",
//                         whiteSpace: "pre-wrap",
//                         wordWrap: "break-word",
//                       }}
//                     >
//                       {msg.content}
//                     </p>
//                   </div>
//                 </div>
//               </div>
//             ))}
//             {isLoading && (
//               <div
//                 style={{
//                   padding: "28px 24px",
//                   backgroundColor: theme.bgAlt,
//                   borderBottom: `1px solid ${theme.border}`,
//                 }}
//               >
//                 <div
//                   style={{
//                     display: "flex",
//                     gap: "20px",
//                     maxWidth: "900px",
//                     margin: "0 auto",
//                     flexDirection: isRTL ? "row-reverse" : "row",
//                   }}
//                 >
//                   <div
//                     style={{
//                       width: "36px",
//                       height: "36px",
//                       borderRadius: "6px",
//                       display: "flex",
//                       alignItems: "center",
//                       justifyContent: "center",
//                       flexShrink: 0,
//                       backgroundColor: theme.accent,
//                       color: "white",
//                       fontSize: "14px",
//                       fontWeight: "600",
//                     }}
//                   >
//                     AI
//                   </div>
//                   <div style={{ flex: 1, paddingTop: "12px" }}>
//                     <div style={{ display: "flex", gap: "4px" }}>
//                       <div
//                         style={{
//                           width: "8px",
//                           height: "8px",
//                           borderRadius: "50%",
//                           backgroundColor: theme.textLight,
//                           animation: "bounce 1.4s infinite ease-in-out both",
//                           animationDelay: "-0.32s",
//                         }}
//                       ></div>
//                       <div
//                         style={{
//                           width: "8px",
//                           height: "8px",
//                           borderRadius: "50%",
//                           backgroundColor: theme.textLight,
//                           animation: "bounce 1.4s infinite ease-in-out both",
//                           animationDelay: "-0.16s",
//                         }}
//                       ></div>
//                       <div
//                         style={{
//                           width: "8px",
//                           height: "8px",
//                           borderRadius: "50%",
//                           backgroundColor: theme.textLight,
//                           animation: "bounce 1.4s infinite ease-in-out both",
//                         }}
//                       ></div>
//                     </div>
//                   </div>
//                 </div>
//               </div>
//             )}
//             <div ref={messagesEndRef} />
//           </div>
//         </div>

//         {/* Input Area */}
//         <div
//           style={{
//             borderTop: `1px solid ${theme.border}`,
//             padding: "20px 24px",
//             backgroundColor: theme.headerBg,
//           }}
//         >
//           <div
//             style={{
//               maxWidth: "900px",
//               margin: "0 auto",
//               width: "100%",
//             }}
//           >
//             {uploadFile && (
//               <div
//                 style={{
//                   marginBottom: "12px",
//                   padding: "10px 14px",
//                   backgroundColor: theme.buttonBg,
//                   borderRadius: "10px",
//                   display: "flex",
//                   alignItems: "center",
//                   gap: "10px",
//                   fontSize: "14px",
//                   color: theme.text,
//                 }}
//               >
//                 <span>📎 {uploadFile.name}</span>
//                 <button
//                   onClick={() => {
//                     setUploadFile(null);
//                     if (fileInputRef.current) fileInputRef.current.value = "";
//                   }}
//                   style={{
//                     marginLeft: "auto",
//                     border: "none",
//                     background: "none",
//                     cursor: "pointer",
//                     fontSize: "18px",
//                     padding: "0 6px",
//                     color: theme.textLight,
//                   }}
//                 >
//                   ✕
//                 </button>
//               </div>
//             )}
//             <div style={{ display: "flex", gap: "10px", alignItems: "flex-end" }}>
//               <div style={{ flex: 1, position: "relative" }}>
//                 <textarea
//                   ref={textareaRef}
//                   style={{
//                     width: "100%",
//                     padding: "14px 50px 14px 16px",
//                     border: `1px solid ${theme.border}`,
//                     borderRadius: "14px",
//                     resize: "none",
//                     fontSize: "15px",
//                     fontFamily: "inherit",
//                     outline: "none",
//                     maxHeight: "200px",
//                     minHeight: "52px",
//                     lineHeight: "1.5",
//                     boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
//                     boxSizing: "border-box",
//                     backgroundColor: theme.bg,
//                     color: theme.text,
//                   }}
//                   placeholder={t.placeholder}
//                   value={input}
//                   onChange={(e) => setInput(e.target.value)}
//                   onKeyDown={handleKeyDown}
//                   rows={1}
//                   disabled={isLoading}
//                 />
//                 <input
//                   type="file"
//                   ref={fileInputRef}
//                   style={{ display: "none" }}
//                   onChange={(e) => setUploadFile(e.target.files[0])}
//                   accept={config.acceptedFiles}
//                 />
//                 <button
//                   onClick={() => fileInputRef.current?.click()}
//                   disabled={isLoading}
//                   style={{
//                     position: "absolute",
//                     right: isRTL ? "auto" : "10px",
//                     left: isRTL ? "10px" : "auto",
//                     bottom: "10px",
//                     border: "none",
//                     background: "none",
//                     cursor: isLoading ? "not-allowed" : "pointer",
//                     padding: "8px",
//                     color: theme.textLight,
//                     fontSize: "20px",
//                     opacity: isLoading ? 0.5 : 1,
//                   }}
//                 >
//                   📎
//                 </button>
//               </div>
//               <button
//                 onClick={sendMessage}
//                 disabled={(!input.trim() && !uploadFile) || isLoading}
//                 style={{
//                   padding: "14px",
//                   border: "none",
//                   borderRadius: "14px",
//                   backgroundColor: (input.trim() || uploadFile) && !isLoading ? "#000000" : theme.buttonBg,
//                   color: (input.trim() || uploadFile) && !isLoading ? "white" : theme.textLight,
//                   cursor: (input.trim() || uploadFile) && !isLoading ? "pointer" : "not-allowed",
//                   fontSize: "20px",
//                   minWidth: "52px",
//                   height: "52px",
//                   display: "flex",
//                   alignItems: "center",
//                   justifyContent: "center",
//                   transition: "all 0.2s",
//                 }}
//               >
//                 ↑
//               </button>
//             </div>
//           </div>
//         </div>
//       </div>

//       <style>{`
//         @keyframes bounce {
//           0%,
//           80%,
//           100% {
//             transform: scale(0);
//             opacity: 0.5;
//           }
//           40% {
//             transform: scale(1);
//             opacity: 1;
//           }
//         }
//         * {
//           box-sizing: border-box;
//         }
//       `}</style>
//     </div>
//   );
// }

// export default App;



import { useState, useRef, useEffect } from "react";
import { Send, Paperclip, Menu, Plus, Trash2, Moon, Sun, Download, Globe, X, Copy, Check } from "lucide-react";

function App() {
  const config = {
    apiEndpoint: "http://localhost:8000/chat",
    acceptedFiles: ".pdf,.doc,.docx,.txt",
  };

  const translations = {
    en: {
      title: "AI Portfolio RAG Assistant",
      placeholder: "Ask me anything about CVs...",
      newChat: "New chat",
      clearChat: "Clear chat",
      darkMode: "Dark mode",
      language: "Language",
      exportChat: "Export chat",
      history: "Recent chats",
      noHistory: "No previous conversations",
      typing: "Typing",
      error: "Something went wrong",
      copy: "Copy",
      copied: "Copied!",
    },
    fr: {
      title: "Assistant RAG Portfolio IA",
      placeholder: "Posez-moi une question sur les CV...",
      newChat: "Nouvelle discussion",
      clearChat: "Effacer la discussion",
      darkMode: "Mode sombre",
      language: "Langue",
      exportChat: "Exporter",
      history: "Discussions récentes",
      noHistory: "Aucune conversation précédente",
      typing: "Tape",
      error: "Une erreur s'est produite",
      copy: "Copier",
      copied: "Copié!",
    },
    ar: {
      title: "مساعد السيرة الذاتية بالذكاء الاصطناعي",
      placeholder: "اسألني أي شيء عن السير الذاتية...",
      newChat: "محادثة جديدة",
      clearChat: "مسح المحادثة",
      darkMode: "الوضع الداكن",
      language: "اللغة",
      exportChat: "تصدير",
      history: "المحادثات الأخيرة",
      noHistory: "لا توجد محادثات سابقة",
      typing: "يكتب",
      error: "حدث خطأ ما",
      copy: "نسخ",
      copied: "تم النسخ!",
    },
  };

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! I'm your CV Assistant. I can help you:\n\n• Analyze and structure CVs\n• Extract key information\n• Compare candidates\n• Answer questions about resumes\n\nHow can I help you today?",
    },
  ]);
  const [conversations, setConversations] = useState([]);
  const [currentConversationId, setCurrentConversationId] = useState(Date.now());
  const [input, setInput] = useState("");
  const [uploadFile, setUploadFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true);
  const [language, setLanguage] = useState("en");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState(null);

  const fileInputRef = useRef(null);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const t = translations[language];
  const isRTL = language === "ar";

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + "px";
    }
  }, [input]);

  const theme = darkMode
    ? {
        bg: "#212121",
        surface: "#2f2f2f",
        surfaceHover: "#3a3a3a",
        text: "#ececec",
        textSecondary: "#b4b4b4",
        border: "#444444",
        accent: "#19c37d",
        userBg: "#2f2f2f",
        assistantBg: "#212121",
        shadow: "rgba(0, 0, 0, 0.3)",
      }
    : {
        bg: "#ffffff",
        surface: "#f7f7f8",
        surfaceHover: "#ececec",
        text: "#0d0d0d",
        textSecondary: "#676767",
        border: "#e5e5e5",
        accent: "#10a37f",
        userBg: "#f7f7f8",
        assistantBg: "#ffffff",
        shadow: "rgba(0, 0, 0, 0.1)",
      };

  const saveCurrentConversation = () => {
    if (messages.length <= 1) return;
    setConversations((prev) => {
      const filtered = prev.filter((c) => c.id !== currentConversationId);
      return [
        { id: currentConversationId, messages, timestamp: Date.now() },
        ...filtered,
      ].slice(0, 20);
    });
  };

  const startNewChat = () => {
    saveCurrentConversation();
    setMessages([
      {
        role: "assistant",
        content: "Hello! I'm your CV Assistant. How can I help you today?",
      },
    ]);
    setCurrentConversationId(Date.now());
    setInput("");
    setUploadFile(null);
    setSidebarOpen(false);
  };

  const loadConversation = (id) => {
    const conv = conversations.find((c) => c.id === id);
    if (conv) {
      saveCurrentConversation();
      setMessages(conv.messages);
      setCurrentConversationId(id);
      setSidebarOpen(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() && !uploadFile) return;

    const userMessage = input.trim();
    const newMessages = [...messages];

    if (userMessage) {
      newMessages.push({ role: "user", content: userMessage });
    }
    if (uploadFile) {
      newMessages.push({ role: "user", content: `📎 ${uploadFile.name}` });
    }

    setMessages(newMessages);
    setInput("");
    const currentFile = uploadFile;
    setUploadFile(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append("message", userMessage);
      formData.append("format_type", "markdown");
      if (currentFile) {
        formData.append("file", currentFile);
      }

      const response = await fetch(config.apiEndpoint, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Network error");

      const data = await response.json();
      const aiResponse = data.reply || data.response || data.message || "I apologize, but I couldn't process that request.";
      
      setMessages((prev) => [...prev, { role: "assistant", content: aiResponse }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `❌ ${t.error}: ${error.message}` },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        role: "assistant",
        content: "Chat cleared. How can I help you?",
      },
    ]);
    setSidebarOpen(false);
  };

  const exportChat = () => {
    const text = messages
      .map((m) => `${m.role.toUpperCase()}: ${m.content}`)
      .join("\n\n");
    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `cv-assistant-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    setSidebarOpen(false);
  };

  const copyToClipboard = (text, index) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const formatContent = (content) => {
    const lines = content.split('\n');
    return lines.map((line, i) => {
      // Headers
      if (line.startsWith('### ')) {
        return <h3 key={i} style={{ fontSize: '16px', fontWeight: '600', margin: '16px 0 8px', color: theme.text }}>{line.replace('### ', '')}</h3>;
      }
      if (line.startsWith('## ')) {
        return <h2 key={i} style={{ fontSize: '18px', fontWeight: '600', margin: '20px 0 10px', color: theme.text }}>{line.replace('## ', '')}</h2>;
      }
      if (line.startsWith('# ')) {
        return <h1 key={i} style={{ fontSize: '22px', fontWeight: '700', margin: '24px 0 12px', color: theme.text }}>{line.replace('# ', '')}</h1>;
      }
      
      // Lists
      if (line.startsWith('- ') || line.startsWith('• ')) {
        return <li key={i} style={{ marginLeft: '20px', marginBottom: '4px', color: theme.text }}>{line.replace(/^[-•]\s*/, '')}</li>;
      }
      
      // Bold text
      if (line.includes('**')) {
        const parts = line.split('**');
        return (
          <p key={i} style={{ margin: '8px 0', color: theme.text, lineHeight: '1.6' }}>
            {parts.map((part, j) => j % 2 === 1 ? <strong key={j}>{part}</strong> : part)}
          </p>
        );
      }
      
      // Code blocks
      if (line.startsWith('```')) {
        return null;
      }
      
      // Regular text
      if (line.trim()) {
        return <p key={i} style={{ margin: '8px 0', color: theme.text, lineHeight: '1.6' }}>{line}</p>;
      }
      
      return <br key={i} />;
    });
  };

  return (
    <div
      style={{
        display: "flex",
        width: "100vw",
        height: "100vh",
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif",
        backgroundColor: theme.bg,
        color: theme.text,
        direction: isRTL ? "rtl" : "ltr",
      }}
    >
      {/* Sidebar */}
      <div
        style={{
          width: sidebarOpen ? "260px" : "0",
          backgroundColor: theme.surface,
          transition: "width 0.2s ease",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
          borderRight: `1px solid ${theme.border}`,
        }}
      >
        <div style={{ padding: "12px", borderBottom: `1px solid ${theme.border}` }}>
          <button
            onClick={startNewChat}
            style={{
              width: "100%",
              padding: "10px",
              backgroundColor: theme.surfaceHover,
              border: `1px solid ${theme.border}`,
              borderRadius: "8px",
              cursor: "pointer",
              fontSize: "14px",
              color: theme.text,
              display: "flex",
              alignItems: "center",
              gap: "8px",
              justifyContent: "center",
              transition: "all 0.2s",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = theme.border)}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = theme.surfaceHover)}
          >
            <Plus size={16} /> {t.newChat}
          </button>
        </div>

        <div style={{ flex: 1, overflowY: "auto", padding: "8px" }}>
          <div style={{ fontSize: "12px", color: theme.textSecondary, padding: "8px 12px", fontWeight: "500" }}>
            {t.history}
          </div>
          {conversations.length === 0 ? (
            <div style={{ padding: "12px", fontSize: "13px", color: theme.textSecondary }}>
              {t.noHistory}
            </div>
          ) : (
            conversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => loadConversation(conv.id)}
                style={{
                  width: "100%",
                  padding: "10px 12px",
                  backgroundColor: conv.id === currentConversationId ? theme.surfaceHover : "transparent",
                  border: "none",
                  borderRadius: "8px",
                  cursor: "pointer",
                  fontSize: "13px",
                  color: theme.text,
                  textAlign: isRTL ? "right" : "left",
                  marginBottom: "4px",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                  transition: "all 0.15s",
                }}
                onMouseEnter={(e) => {
                  if (conv.id !== currentConversationId) {
                    e.currentTarget.style.backgroundColor = theme.surfaceHover;
                  }
                }}
                onMouseLeave={(e) => {
                  if (conv.id !== currentConversationId) {
                    e.currentTarget.style.backgroundColor = "transparent";
                  }
                }}
              >
                {conv.messages[1]?.content.substring(0, 30) || "New conversation"}
              </button>
            ))
          )}
        </div>

        <div style={{ padding: "12px", borderTop: `1px solid ${theme.border}` }}>
          <button
            onClick={() => setDarkMode(!darkMode)}
            style={{
              width: "100%",
              padding: "10px",
              backgroundColor: "transparent",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontSize: "13px",
              color: theme.text,
              display: "flex",
              alignItems: "center",
              gap: "10px",
              marginBottom: "6px",
              transition: "all 0.15s",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = theme.surfaceHover)}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
          >
            {darkMode ? <Sun size={16} /> : <Moon size={16} />}
            {t.darkMode}
          </button>

          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            style={{
              width: "100%",
              padding: "10px",
              backgroundColor: theme.surfaceHover,
              border: `1px solid ${theme.border}`,
              borderRadius: "8px",
              color: theme.text,
              cursor: "pointer",
              fontSize: "13px",
              marginBottom: "6px",
            }}
          >
            <option value="en">🇬🇧 English</option>
            <option value="fr">🇫🇷 Français</option>
            <option value="ar">🇸🇦 العربية</option>
          </select>

          <button
            onClick={clearChat}
            style={{
              width: "100%",
              padding: "10px",
              backgroundColor: "transparent",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontSize: "13px",
              color: theme.text,
              display: "flex",
              alignItems: "center",
              gap: "10px",
              marginBottom: "6px",
              transition: "all 0.15s",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = theme.surfaceHover)}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
          >
            <Trash2 size={16} />
            {t.clearChat}
          </button>

          <button
            onClick={exportChat}
            style={{
              width: "100%",
              padding: "10px",
              backgroundColor: "transparent",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontSize: "13px",
              color: theme.text,
              display: "flex",
              alignItems: "center",
              gap: "10px",
              transition: "all 0.15s",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = theme.surfaceHover)}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
          >
            <Download size={16} />
            {t.exportChat}
          </button>
        </div>
      </div>

      {/* Main Chat */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        {/* Header */}
        <div
          style={{
            padding: "12px 16px",
            borderBottom: `1px solid ${theme.border}`,
            display: "flex",
            alignItems: "center",
            gap: "12px",
            backgroundColor: theme.surface,
          }}
        >
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            style={{
              padding: "8px",
              backgroundColor: "transparent",
              border: "none",
              cursor: "pointer",
              borderRadius: "6px",
              color: theme.text,
              display: "flex",
              alignItems: "center",
              transition: "all 0.15s",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = theme.surfaceHover)}
            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
          >
            <Menu size={20} />
          </button>
          <h1 style={{ margin: 0, fontSize: "16px", fontWeight: "600" }}>
            {t.title}
          </h1>
        </div>

        {/* Messages */}
        <div
          style={{
            flex: 1,
            overflowY: "auto",
            backgroundColor: theme.bg,
          }}
        >
          {messages.map((msg, idx) => (
            <div
              key={idx}
              style={{
                padding: "24px",
                backgroundColor: msg.role === "assistant" ? theme.assistantBg : theme.userBg,
                borderBottom: `1px solid ${theme.border}`,
              }}
            >
              <div
                style={{
                  maxWidth: "768px",
                  margin: "0 auto",
                  display: "flex",
                  gap: "16px",
                  flexDirection: isRTL ? "row-reverse" : "row",
                }}
              >
                <div
                  style={{
                    width: "32px",
                    height: "32px",
                    borderRadius: "50%",
                    backgroundColor: msg.role === "assistant" ? theme.accent : "#5436da",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexShrink: 0,
                    fontSize: "14px",
                    fontWeight: "600",
                    color: "white",
                  }}
                >
                  {msg.role === "assistant" ? "AI" : "U"}
                </div>
                <div style={{ flex: 1, minWidth: 0, position: "relative", paddingRight: msg.role === "assistant" ? "40px" : "0" }}>
                  <div style={{ fontSize: "15px", lineHeight: "1.7" }}>
                    {formatContent(msg.content)}
                  </div>
                  {msg.role === "assistant" && (
                    <button
                      onClick={() => copyToClipboard(msg.content, idx)}
                      style={{
                        position: "absolute",
                        top: "0",
                        right: isRTL ? "auto" : "0",
                        left: isRTL ? "0" : "auto",
                        padding: "6px",
                        backgroundColor: "transparent",
                        border: "none",
                        cursor: "pointer",
                        borderRadius: "6px",
                        color: theme.textSecondary,
                        display: "flex",
                        alignItems: "center",
                        gap: "4px",
                        fontSize: "12px",
                        transition: "all 0.15s",
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.backgroundColor = theme.surfaceHover;
                        e.currentTarget.style.color = theme.text;
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.backgroundColor = "transparent";
                        e.currentTarget.style.color = theme.textSecondary;
                      }}
                    >
                      {copiedIndex === idx ? (
                        <>
                          <Check size={14} /> {t.copied}
                        </>
                      ) : (
                        <>
                          <Copy size={14} /> {t.copy}
                        </>
                      )}
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div
              style={{
                padding: "24px",
                backgroundColor: theme.assistantBg,
                borderBottom: `1px solid ${theme.border}`,
              }}
            >
              <div
                style={{
                  maxWidth: "768px",
                  margin: "0 auto",
                  display: "flex",
                  gap: "16px",
                  flexDirection: isRTL ? "row-reverse" : "row",
                }}
              >
                <div
                  style={{
                    width: "32px",
                    height: "32px",
                    borderRadius: "50%",
                    backgroundColor: theme.accent,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexShrink: 0,
                    fontSize: "14px",
                    fontWeight: "600",
                    color: "white",
                  }}
                >
                  AI
                </div>
                <div style={{ flex: 1, paddingTop: "6px" }}>
                  <div style={{ display: "flex", gap: "6px" }}>
                    {[0, 1, 2].map((i) => (
                      <div
                        key={i}
                        style={{
                          width: "8px",
                          height: "8px",
                          borderRadius: "50%",
                          backgroundColor: theme.textSecondary,
                          animation: "bounce 1.4s infinite ease-in-out both",
                          animationDelay: `${-0.32 + i * 0.16}s`,
                        }}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div
          style={{
            padding: "16px",
            borderTop: `1px solid ${theme.border}`,
            backgroundColor: theme.surface,
          }}
        >
          <div style={{ maxWidth: "768px", margin: "0 auto" }}>
            {uploadFile && (
              <div
                style={{
                  marginBottom: "12px",
                  padding: "10px 14px",
                  backgroundColor: theme.surfaceHover,
                  borderRadius: "10px",
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  fontSize: "14px",
                }}
              >
                <Paperclip size={16} />
                <span style={{ flex: 1 }}>{uploadFile.name}</span>
                <button
                  onClick={() => {
                    setUploadFile(null);
                    if (fileInputRef.current) fileInputRef.current.value = "";
                  }}
                  style={{
                    border: "none",
                    background: "none",
                    cursor: "pointer",
                    padding: "4px",
                    color: theme.textSecondary,
                    display: "flex",
                  }}
                >
                  <X size={16} />
                </button>
              </div>
            )}

            <div style={{ display: "flex", gap: "8px", alignItems: "flex-end" }}>
              <div style={{ flex: 1, position: "relative" }}>
                <textarea
                  ref={textareaRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder={t.placeholder}
                  disabled={isLoading}
                  style={{
                    width: "100%",
                    padding: "12px 44px 12px 16px",
                    border: `1px solid ${theme.border}`,
                    borderRadius: "12px",
                    resize: "none",
                    fontSize: "15px",
                    fontFamily: "inherit",
                    outline: "none",
                    minHeight: "52px",
                    maxHeight: "200px",
                    backgroundColor: theme.bg,
                    color: theme.text,
                    boxShadow: `0 0 0 1px ${theme.shadow}`,
                  }}
                  rows={1}
                />
                <input
                  ref={fileInputRef}
                  type="file"
                  style={{ display: "none" }}
                  accept={config.acceptedFiles}
                  onChange={(e) => setUploadFile(e.target.files[0])}
                />
                <button
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isLoading}
                  style={{
                    position: "absolute",
                    right: isRTL ? "auto" : "10px",
                    left: isRTL ? "10px" : "auto",
                    bottom: "12px",
                    border: "none",
                    background: "none",
                    cursor: isLoading ? "not-allowed" : "pointer",
                    padding: "6px",
                    color: theme.textSecondary,
                    display: "flex",
                    opacity: isLoading ? 0.5 : 1,
                  }}
                >
                  <Paperclip size={20} />
                </button>
              </div>

              <button
                onClick={sendMessage}
                disabled={(!input.trim() && !uploadFile) || isLoading}
                style={{
                  width: "52px",
                  height: "52px",
                  border: "none",
                  borderRadius: "12px",
                  backgroundColor:
                    input.trim() || uploadFile ? theme.accent : theme.surfaceHover,
                  color: input.trim() || uploadFile ? "white" : theme.textSecondary,
                  cursor:
                    input.trim() || uploadFile && !isLoading ? "pointer" : "not-allowed",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  transition: "all 0.2s",
                  flexShrink: 0,
                }}
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes bounce {
          0%, 80%, 100% {
            transform: scale(0);
            opacity: 0.5;
          }
          40% {
            transform: scale(1);
            opacity: 1;
          }
        }
        
        * {
          box-sizing: border-box;
        }
        
        ::-webkit-scrollbar {
          width: 8px;
        }
        
        ::-webkit-scrollbar-track {
          background: ${theme.surface};
        }
        
        ::-webkit-scrollbar-thumb {
          background: ${theme.border};
          border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
          background: ${theme.textSecondary};
        }
      `}</style>
    </div>
  );
}

export default App;