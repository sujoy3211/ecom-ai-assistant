import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";

function ProductCard({ product, index }) {
  const q = encodeURIComponent(product.name);
  const platforms = [
    { name: "Amazon", url: "https://www.amazon.in/s?k=" + q, color: "#FF9900" },
    { name: "Flipkart", url: "https://www.flipkart.com/search?q=" + q, color: "#F37220" },
    { name: "Meesho", url: "https://www.meesho.com/search?q=" + q, color: "#9B2FF7" },
    { name: "Myntra", url: "https://www.myntra.com/" + q, color: "#FF3F6C" },
    { name: "Snapdeal", url: "https://www.snapdeal.com/search?keyword=" + q, color: "#E40000" },
    { name: "Croma", url: "https://www.croma.com/searchB?q=" + q, color: "#1B5E20" },
    { name: "Reliance", url: "https://www.reliancedigital.in/search?q=" + q, color: "#0066CC" },
    { name: "Nykaa", url: "https://www.nykaa.com/search/result/?q=" + q, color: "#FC2779" },
    { name: "Tata Cliq", url: "https://www.tatacliq.com/search/?text=" + q, color: "#8B0000" },
    { name: "Ajio", url: "https://www.ajio.com/search/?text=" + q, color: "#FF6B35" },
    { name: "JioMart", url: "https://www.jiomart.com/search/" + q, color: "#0F4C81" },
    { name: "Shopsy", url: "https://shopsy.in/search?q=" + q, color: "#F5A623" },
  ];

  const [showAll, setShowAll] = useState(false);
  const [wishlisted, setWishlisted] = useState(false);
  const visible = showAll ? platforms : platforms.slice(0, 4);

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.1 }}
      style={{
        background: product.is_best_deal ? "rgba(34,197,94,0.1)" : "rgba(99,102,241,0.08)",
        border: product.is_best_deal ? "1px solid rgba(34,197,94,0.4)" : "1px solid rgba(99,102,241,0.25)",
        borderRadius: "12px", padding: "12px", marginTop: "8px",
        display: "flex", gap: "12px", alignItems: "flex-start"
      }}
    >
      {product.thumbnail && (
        <img
          src={product.thumbnail}
          alt={product.name}
          style={{
            width: "65px", height: "65px", objectFit: "contain",
            borderRadius: "8px", background: "rgba(255,255,255,0.08)",
            padding: "4px", flexShrink: 0
          }}
        />
      )}
      <div style={{ flex: 1 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <p style={{ color: "#e0e7ff", fontWeight: 600, fontSize: "13px", marginBottom: "4px", flex: 1 }}>
            {product.name?.length > 60 ? product.name.substring(0, 60) + "..." : product.name}
          </p>
          <motion.button
            whileHover={{ scale: 1.2 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => setWishlisted(!wishlisted)}
            style={{ background: "none", border: "none", cursor: "pointer", fontSize: "18px", marginLeft: "8px" }}
          >
            {wishlisted ? "❤️" : "🤍"}
          </motion.button>
        </div>

        {product.is_best_deal && (
          <div style={{
            background: "rgba(34,197,94,0.2)", border: "1px solid rgba(34,197,94,0.4)",
            borderRadius: "6px", padding: "2px 8px", display: "inline-block", marginBottom: "6px"
          }}>
            <span style={{ color: "#22c55e", fontSize: "11px", fontWeight: 700 }}>🏆 Best Deal</span>
          </div>
        )}

        <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px", flexWrap: "wrap" }}>
          <span style={{
            background: product.is_best_deal ? "linear-gradient(135deg, #22c55e, #16a34a)" : "linear-gradient(135deg, #6366f1, #8b5cf6)",
            color: "white", padding: "2px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: 700
          }}>
            {product.price}
          </span>
          {product.source && <span style={{ color: "#64748b", fontSize: "11px" }}>🏪 {product.source}</span>}
          {product.rating && <span style={{ color: "#fbbf24", fontSize: "11px" }}>⭐ {product.rating}</span>}
        </div>

        {product.link && (
          <a
            href={product.link}
            target="_blank"
            rel="noreferrer"
            style={{
              display: "inline-block",
              background: product.is_best_deal ? "linear-gradient(135deg, #22c55e, #16a34a)" : "linear-gradient(135deg, #6366f1, #8b5cf6)",
              color: "white", padding: "5px 14px", borderRadius: "6px",
              fontSize: "12px", textDecoration: "none", fontWeight: 700,
              marginBottom: "8px", marginRight: "6px"
            }}
          >
            Buy on {product.source} →
          </a>
        )}

        <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
          {visible.map((p, i) => (
            <a
              key={i}
              href={p.url}
              target="_blank"
              rel="noreferrer"
              style={{
                background: p.color, color: "white",
                padding: "3px 10px", borderRadius: "6px",
                fontSize: "10px", textDecoration: "none", fontWeight: 600
              }}
            >
              {p.name}
            </a>
          ))}
          <button
            onClick={() => setShowAll(!showAll)}
            style={{
              background: "rgba(99,102,241,0.2)", border: "1px solid rgba(99,102,241,0.4)",
              color: "#818cf8", padding: "3px 10px", borderRadius: "6px",
              fontSize: "10px", cursor: "pointer", fontWeight: 600
            }}
          >
            {showAll ? "Less" : "More +"}
          </button>
        </div>
      </div>
    </motion.div>
  );
}


function Message({ msg }) {
  const isUser = msg.role === "user";
  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.3 }}
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        marginBottom: "16px"
      }}
    >
      <div style={{ maxWidth: "75%" }}>
        {!isUser && (
          <div style={{ display: "flex", alignItems: "center", marginBottom: "6px" }}>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
              style={{
                width: "28px", height: "28px", borderRadius: "50%",
                background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
                display: "flex", alignItems: "center",
                justifyContent: "center", fontSize: "14px", marginRight: "8px"
              }}
            >🤖</motion.div>
            <span style={{ color: "#818cf8", fontSize: "12px" }}>AI Assistant</span>
          </div>
        )}
        <div style={{
          background: isUser
            ? "linear-gradient(135deg, #6366f1, #8b5cf6)"
            : "rgba(255,255,255,0.05)",
          border: isUser ? "none" : "1px solid rgba(255,255,255,0.1)",
          borderRadius: isUser ? "20px 20px 4px 20px" : "20px 20px 20px 4px",
          padding: "12px 16px", color: "white",
          fontSize: "14px", lineHeight: "1.6",
        }}>
          {msg.content}
        </div>
        {msg.products && msg.products.length > 0 && (
          <div style={{ marginTop: "8px" }}>
            {msg.products.map((p, i) => (
              <ProductCard key={i} product={p} index={i} />
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}

export default function App() {
  const [messages, setMessages] = useState([{
    role: "assistant",
    content: "👋 Hi! I'm your AI shopping assistant. Ask me about ANY product — I'll search the internet and find the best deals for you!",
    products: []
  }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const userMsg = { role: "user", content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const res = await axios.post("https://ecom-ai-assistant-nf73.onrender.com/api/chat", { message: input });
      setMessages(prev => [...prev, {
        role: "assistant",
        content: res.data.answer,
        products: res.data.relevant_products
      }]);
    } catch {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Something went wrong. Please try again.",
        products: []
      }]);
    } finally {
      setLoading(false);
    }
  };

  const orbs = [
    { size: 300, left: "5%", top: "10%", color: "rgba(99,102,241,0.25)", duration: 8 },
    { size: 200, left: "80%", top: "5%", color: "rgba(139,92,246,0.2)", duration: 10 },
    { size: 250, left: "60%", top: "60%", color: "rgba(236,72,153,0.15)", duration: 12 },
    { size: 180, left: "20%", top: "70%", color: "rgba(99,102,241,0.2)", duration: 9 },
    { size: 220, left: "40%", top: "30%", color: "rgba(139,92,246,0.15)", duration: 11 },
  ];

  return (
    <>
      <div style={{
        position: "fixed", top: 0, left: 0, width: "100%", height: "100%",
        background: "#0a0a0f", zIndex: 0
      }} />

      {orbs.map((orb, i) => (
        <motion.div
          key={i}
          animate={{ x: [0, 40, -20, 0], y: [0, -50, 30, 0], scale: [1, 1.2, 0.9, 1] }}
          transition={{ duration: orb.duration, repeat: Infinity, ease: "easeInOut", delay: i * 1.5 }}
          style={{
            position: "fixed",
            width: orb.size + "px", height: orb.size + "px",
            borderRadius: "50%",
            background: "radial-gradient(circle, " + orb.color + ", transparent)",
            left: orb.left, top: orb.top,
            zIndex: 0, pointerEvents: "none", filter: "blur(40px)"
          }}
        />
      ))}

      <div style={{
        position: "fixed", top: 0, left: 0, width: "100%", height: "100%",
        backgroundImage: "linear-gradient(rgba(99,102,241,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(99,102,241,0.03) 1px, transparent 1px)",
        backgroundSize: "50px 50px",
        zIndex: 0, pointerEvents: "none"
      }} />

      <div style={{
        position: "relative", zIndex: 1,
        display: "flex", flexDirection: "column",
        alignItems: "center", minHeight: "100vh", padding: "20px"
      }}>

        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          style={{ textAlign: "center", marginBottom: "24px", marginTop: "30px" }}
        >
          <motion.div
            animate={{ opacity: [0.7, 1, 0.7] }}
            transition={{ duration: 2, repeat: Infinity }}
            style={{
              display: "inline-block",
              background: "rgba(99,102,241,0.15)",
              border: "1px solid rgba(99,102,241,0.4)",
              borderRadius: "20px", padding: "4px 16px",
              color: "#818cf8", fontSize: "12px", marginBottom: "12px"
            }}
          >
            Searches real products from the internet
          </motion.div>
          <h1 style={{
            fontSize: "clamp(1.8rem, 5vw, 3rem)", fontWeight: 800,
            background: "linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899)",
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
            lineHeight: 1.2
          }}>
            AI Shopping Assistant
          </h1>
          <p style={{ color: "#475569", marginTop: "8px", fontSize: "14px" }}>
            Ask me anything — I will find the best deals online!
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          style={{
            width: "100%", maxWidth: "780px",
            background: "rgba(10,10,25,0.85)",
            border: "1px solid rgba(99,102,241,0.25)",
            borderRadius: "24px",
            backdropFilter: "blur(20px)",
            display: "flex", flexDirection: "column",
            height: "62vh",
            boxShadow: "0 0 80px rgba(99,102,241,0.15)"
          }}
        >
          <div style={{
            padding: "16px 24px",
            borderBottom: "1px solid rgba(99,102,241,0.15)",
            display: "flex", alignItems: "center", gap: "10px"
          }}>
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              style={{
                width: "10px", height: "10px", borderRadius: "50%",
                background: "#22c55e", boxShadow: "0 0 8px #22c55e"
              }}
            />
            <span style={{ color: "#64748b", fontSize: "13px" }}>AI is online - Powered by Groq LLaMA 3.3</span>
          </div>

          <div style={{ flex: 1, overflowY: "auto", padding: "24px" }}>
            <AnimatePresence>
              {messages.map((msg, i) => (
                <Message key={i} msg={msg} />
              ))}
            </AnimatePresence>
            {loading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                style={{ display: "flex", alignItems: "center", gap: "8px" }}
              >
                <div style={{
                  width: "28px", height: "28px", borderRadius: "50%",
                  background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
                  display: "flex", alignItems: "center", justifyContent: "center", fontSize: "14px"
                }}>🤖</div>
                <div style={{ display: "flex", gap: "4px" }}>
                  {[0, 1, 2].map(j => (
                    <motion.div
                      key={j}
                      animate={{ y: [0, -6, 0] }}
                      transition={{ duration: 0.6, repeat: Infinity, delay: j * 0.15 }}
                      style={{ width: "6px", height: "6px", borderRadius: "50%", background: "#6366f1" }}
                    />
                  ))}
                </div>
              </motion.div>
            )}
            <div ref={bottomRef} />
          </div>

          <div style={{
            padding: "16px 24px",
            borderTop: "1px solid rgba(99,102,241,0.15)",
            display: "flex", gap: "12px", alignItems: "center"
          }}>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === "Enter" && sendMessage()}
              placeholder="e.g. Best laptop under 55000 or wireless headphones"
              style={{
                flex: 1, background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(99,102,241,0.25)",
                borderRadius: "14px", padding: "13px 18px",
                color: "white", fontSize: "14px", outline: "none",
              }}
              onFocus={e => e.target.style.borderColor = "rgba(99,102,241,0.6)"}
              onBlur={e => e.target.style.borderColor = "rgba(99,102,241,0.25)"}
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={sendMessage}
              disabled={loading}
              style={{
                background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
                border: "none", borderRadius: "14px",
                padding: "13px 28px", color: "white",
                fontWeight: 700, cursor: loading ? "not-allowed" : "pointer",
                fontSize: "14px", opacity: loading ? 0.7 : 1,
                whiteSpace: "nowrap"
              }}
            >
              {loading ? "..." : "Send"}
            </motion.button>
          </div>
        </motion.div>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          style={{ color: "#1e293b", marginTop: "20px", fontSize: "12px" }}
        >
          Built with FastAPI - SerpAPI - Groq LLaMA 3.3 - React
        </motion.p>
      </div>
    </>
  );
}
