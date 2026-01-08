"use client";

import { useState, useEffect } from "react";

// --- 0. 工具 ---
const Typewriter = ({ text, delay = 30 }: { text: string, delay?: number }) => {
  const [currentText, setCurrentText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (currentIndex < text.length) {
      const timeout = setTimeout(() => {
        setCurrentText(prev => prev + text[currentIndex]);
        setCurrentIndex(prev => prev + 1);
      }, delay);
      return () => clearTimeout(timeout);
    }
  }, [currentIndex, delay, text]);

  return <span>{currentText}</span>;
};

// --- 1. 配置：篇幅选项 ---
const LENGTH_OPTIONS = [
  { id: "short", label: "Brief", range: "4-6 P", value: 5 },
  { id: "medium", label: "Moderate", range: "7-9 P", value: 8 },
  { id: "long", label: "Detailed", range: "10-12 P", value: 11 }
];

// --- 2. 配置：皮肤风格  ---
const THEMES = {
  academic: { 
    id: "academic", name: "Academic", emoji: "🎓",
    bgCover: "/bg-academic-cover.png",     
    bgContent: "/bg-academic-content.png", 
    fontColor: "text-blue-600", bodyColor: "text-slate-600", accentColor: "text-blue-400",
    alignCover: "items-end justify-center text-right pr-12 pb-12", 
    alignContent: "items-start text-left pl-8 pt-8", 
  },
  business: { 
    id: "business", name: "Business", emoji: "⚡",
    bgCover: "/bg-business-cover.png", bgContent: "/bg-business-content.png",
    fontColor: "text-gray-900", bodyColor: "text-gray-700", accentColor: "text-red-600",
    alignCover: "items-start justify-center text-left pl-12", 
    alignContent: "items-start text-left pl-8 pt-8", 
  },
  teaching: { 
    id: "teaching", name: "Teaching", emoji: "🎨",
    bgCover: "/bg-teaching-cover.png", bgContent: "/bg-teaching-content.png",
    fontColor: "text-white", bodyColor: "text-gray-100", accentColor: "text-yellow-400",
    alignCover: "items-center justify-center text-center", 
    alignContent: "items-center text-center pt-10", 
  }
};

// --- 3. 核心渲染器 ---
const RenderSlide = ({ slide, index, themeKey }: { slide: any, index: number, themeKey: string }) => {
  const t = THEMES[themeKey as keyof typeof THEMES];
  const isCover = slide.layout === "title_cover";
  const bgImage = isCover ? t.bgCover : t.bgContent;
  const isDarkTheme = themeKey === 'teaching';
  
  // 统一的半透明容器背景
  const containerBg = isDarkTheme ? "bg-white/10 border-white/20 text-white" : "bg-white/80 border-gray-300 text-gray-800";

  const renderContent = () => {
    // 1. 图表
    if (slide.layout === "chart" && slide.chart_data) {
      return (
        <div className="w-full h-full flex flex-col justify-center items-center">
           <div className={`p-4 rounded-xl border shadow-sm backdrop-blur-sm w-3/4 ${containerBg}`}>
              <div className={`text-xs text-center mb-2 uppercase tracking-widest font-bold ${isDarkTheme ? 'text-gray-300' : 'text-gray-500'}`}>[ {slide.chart_data.chart_type} CHART ]</div>
              <div className={`flex items-end justify-around h-32 gap-2 px-4 pb-2 border-b ${isDarkTheme ? 'border-white/30' : 'border-gray-400'}`}>
                  {slide.chart_data.values.map((val: number, i: number) => (
                      <div key={i} className={`w-8 rounded-t-sm relative group ${themeKey === 'business' ? 'bg-red-600' : themeKey === 'academic' ? 'bg-blue-500' : 'bg-yellow-400'}`} style={{ height: `${Math.min((val / Math.max(...slide.chart_data.values)) * 100, 100)}%` }}>
                      </div>
                  ))}
              </div>
              <div className={`flex justify-around text-[10px] mt-2 font-bold ${isDarkTheme ? 'text-gray-300' : 'text-gray-600'}`}>
                  {slide.chart_data.labels.map((lbl: string, i: number) => <span key={i}>{lbl}</span>)}
              </div>
           </div>
        </div>
      );
    }
    
    // 2. 表格
    if (slide.layout === "table" && slide.table_data) {
        return (
            <div className="w-full px-8 mt-4">
                <div className={`overflow-hidden rounded border shadow-sm ${containerBg} ${isDarkTheme ? 'bg-black/20' : 'bg-white/90'}`}>
                    <table className="w-full text-xs text-left">
                        <thead className={`${themeKey === 'business' ? 'bg-red-100 text-red-900' : themeKey === 'academic' ? 'bg-blue-100 text-blue-900' : 'bg-white/20 text-yellow-300'}`}>
                            <tr>{slide.table_data.headers.map((h: string, i: number) => <th key={i} className={`p-2 font-bold border-b ${isDarkTheme ? 'border-white/20' : 'border-gray-300'}`}>{h}</th>)}</tr>
                        </thead>
                        <tbody className={`divide-y ${isDarkTheme ? 'divide-white/10' : 'divide-gray-300'}`}>
                            {slide.table_data.rows.map((row: any[], i: number) => (
                                <tr key={i}>{row.map((cell, j) => <td key={j} className={`p-2 ${isDarkTheme ? 'text-gray-200' : 'text-gray-700'}`}>{cell}</td>)}</tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }

    // 3. 双栏
    if (slide.layout === "two_column" && slide.content) {
        return (
            <div className="grid grid-cols-2 gap-6 h-full px-8 mt-4">
                <div className={`${isDarkTheme ? 'bg-white/10' : 'bg-gray-50/50'} p-4 rounded-lg border ${isDarkTheme ? 'border-white/10' : 'border-gray-200'} backdrop-blur-sm`}>
                    <ul className="space-y-3">
                        {slide.content.content_left?.map((txt: string, i: number) => (
                            <li key={i} className={`text-sm flex gap-2 ${t.bodyColor} font-medium`}>
                                <span className={`font-bold ${t.accentColor}`}>•</span><span>{txt}</span>
                            </li>
                        ))}
                    </ul>
                </div>
                <div className={`${isDarkTheme ? 'bg-white/10' : 'bg-gray-50/50'} p-4 rounded-lg border ${isDarkTheme ? 'border-white/10' : 'border-gray-200'} backdrop-blur-sm`}>
                    <ul className="space-y-3">
                        {slide.content.content_right?.map((txt: string, i: number) => (
                            <li key={i} className={`text-sm flex gap-2 ${t.bodyColor} font-medium`}>
                                <span className={`font-bold ${t.accentColor}`}>•</span><span>{txt}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        );
    }

    // ✨✨✨ 4. 图片  ✨✨✨
    if (slide.visual?.need_image) {
        return (
            <div className="w-full px-8 mt-2 h-48">
                {/* 这是一个美观的虚线框，告诉用户这里会有图 */}
                <div className={`relative w-full h-full rounded-xl border-2 border-dashed flex flex-col items-center justify-center text-center p-6 gap-2 transition-all group hover:scale-[1.02] ${isDarkTheme ? 'border-white/30 bg-white/5' : 'border-gray-300 bg-gray-50'}`}>
                    
                    <span className="text-4xl opacity-80 mb-1">🖼️</span>
                    
                    <div className={`text-sm font-bold ${isDarkTheme ? 'text-white' : 'text-gray-800'}`}>
                        AI Image Placeholder
                    </div>
                    
                    <div className={`text-xs italic opacity-70 line-clamp-2 px-4 ${isDarkTheme ? 'text-gray-300' : 'text-gray-500'}`}>
                        "{slide.visual.image_prompt}"
                    </div>

                    <div className={`text-[10px] uppercase tracking-widest font-bold mt-2 py-1 px-3 rounded-full ${isDarkTheme ? 'bg-white/20 text-white' : 'bg-gray-200 text-gray-600'}`}>
                        Generated in Download
                    </div>
                </div>
            </div>
        )
    }

    // 5. 列表 & 文本
    if (slide.content?.bullet_points) {
        return (
            <div className="px-8 mt-4">
                <ul className="space-y-3">
                    {slide.content.bullet_points.map((point: string, idx: number) => (
                        <li key={idx} className={`text-sm flex gap-3 ${t.bodyColor} font-medium items-start`}>
                            <span className={`font-bold text-lg leading-none ${t.accentColor}`}>•</span>
                            <span className="leading-snug"><Typewriter text={point} delay={10} /></span>
                        </li>
                    ))}
                </ul>
            </div>
        );
    }
    if (slide.content?.text_body) {
        return <p className={`px-8 mt-4 text-sm leading-relaxed ${t.bodyColor} font-medium`}>{slide.content.text_body}</p>;
    }
    return null;
  };

  return (
    <div 
        className="aspect-video relative flex flex-col group hover:scale-[1.01] transition-transform duration-500 rounded-xl overflow-hidden shadow-2xl bg-white"
        style={{
            backgroundImage: `url(${bgImage})`, 
            backgroundSize: 'cover',
            backgroundPosition: 'center'
        }}
    >
        <div className={`absolute inset-0 -z-10 ${themeKey === 'teaching' ? 'bg-zinc-800' : 'bg-white'}`}></div>
        <div className={`relative z-10 h-full flex flex-col w-full`}>
            {isCover ? (
                <div className={`flex-1 flex flex-col w-full h-full ${t.alignCover}`}>
                    <div className={`${themeKey === 'academic' ? 'w-2/3' : 'w-full'}`}>
                        <h1 className={`text-5xl font-extrabold mb-6 ${t.fontColor} drop-shadow-sm leading-tight`}>{slide.title}</h1>
                        <p className={`text-xl ${t.accentColor} font-bold opacity-90`}>{slide.subtitle}</p>
                    </div>
                </div>
            ) : (
                <div className={`flex flex-col w-full h-full ${t.alignContent}`}>
                    <div className="mb-2 w-full">
                        <h3 className={`text-3xl font-bold ${t.fontColor} tracking-tight drop-shadow-sm px-8`}>{slide.title}</h3>
                        <div className={`absolute top-6 right-6 text-[10px] font-mono px-2 py-1 rounded backdrop-blur-sm ${themeKey === 'teaching' ? 'text-white/50 bg-white/10' : 'text-gray-500 bg-white/60'}`}>
                            {index + 1 < 10 ? `0${index + 1}` : index + 1}
                        </div>
                    </div>
                    <div className="flex-1 w-full overflow-hidden">{renderContent()}</div>
                </div>
            )}
        </div>
    </div>
  );
};

// --- 4. 主程序 ---
export default function Home() {
  const [step, setStep] = useState<'input' | 'outline' | 'preview'>('input');
  const [inputValue, setInputValue] = useState("");
  
  const [slideCountObj, setSlideCountObj] = useState(LENGTH_OPTIONS[1]); 
  const [currentTheme, setCurrentTheme] = useState<keyof typeof THEMES>('business');
  const [activeDropdown, setActiveDropdown] = useState<'none' | 'count' | 'theme'>('none');
  
  const [isGenerating, setIsGenerating] = useState(false);
  const [loadingText, setLoadingText] = useState("Initializing...");
  
  const [pptData, setPptData] = useState<any>(null); 
  const [downloadUrl, setDownloadUrl] = useState("");

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if ((e.target as HTMLElement).closest('.dropdown-container')) return;
      setActiveDropdown('none');
    };
    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, []);

  const handleGenerateOutline = async () => {
    if (!inputValue.trim()) return;
    setIsGenerating(true); 
    setLoadingText("Connecting to Brain...");
    try {
        const timer1 = setTimeout(() => setLoadingText("Researching topic..."), 2000);
        const timer2 = setTimeout(() => setLoadingText("Structuring logic..."), 5000);
        
        const res = await fetch('http://127.0.0.1:8000/api/generate_outline', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ 
                topic: inputValue,
                slide_length: slideCountObj.value, 
                theme: currentTheme,
                use_ai: true 
            })
        });
        clearTimeout(timer1);
        clearTimeout(timer2);

        if (!res.ok) throw new Error("Connection failed");
        const jsonRes = await res.json();
        if (jsonRes.status !== "success" || !jsonRes.data) throw new Error("Invalid response");

        setPptData(jsonRes.data); 
        setStep('outline');
    } catch (e: any) {
        alert("Generation Error: " + e.message);
    } finally {
        setIsGenerating(false);
    }
  };

  const handleRenderAndDownload = async () => {
      setIsGenerating(true);
      setLoadingText("Rendering .PPTX file...");
      try {
          const res = await fetch('http://127.0.0.1:8000/api/render_pptx', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ theme: currentTheme, ppt_data: pptData })
        });
        const jsonRes = await res.json();
        if (jsonRes.status === "success" && jsonRes.download_url) {
            setDownloadUrl(jsonRes.download_url);
            setStep('preview');
        } else {
            throw new Error("Render failed");
        }
      } catch(e: any) {
          alert("Rendering failed: " + e.message);
      } finally {
          setIsGenerating(false);
      }
  };

  const t = THEMES[currentTheme];

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 transition-colors duration-1000 bg-black relative overflow-hidden font-sans">
      <div className="absolute inset-0 z-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] pointer-events-none"></div>
      
      {/* --- STEP 1: Input --- */}
      {step === 'input' && (
        <div className="relative z-10 w-full max-w-3xl text-center animate-in fade-in zoom-in duration-500 flex flex-col items-center">
          <h1 className="text-8xl md:text-[9rem] font-bold tracking-tighter bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 text-transparent bg-clip-text animate-pulse mb-6 leading-none select-none">
            SlideGen AI
          </h1>
          <p className="text-gray-400 text-xl font-light tracking-widest mb-16">
             Enter your idea, I'll handle the rest.
          </p>
          <div className="relative w-full max-w-2xl mx-auto">
             <div className="flex gap-3 mb-3 justify-start px-2">
                <div className="relative dropdown-container">
                    <button onClick={() => setActiveDropdown(activeDropdown === 'count' ? 'none' : 'count')} className={`flex items-center gap-2 px-4 py-2 rounded-full border text-xs font-bold transition-all backdrop-blur-md ${activeDropdown === 'count' ? "bg-purple-600 text-white border-purple-500 shadow-[0_0_15px_rgba(168,85,247,0.5)]" : "bg-white/5 text-gray-300 border-white/10 hover:bg-white/10"}`}>
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                        {slideCountObj.label} ({slideCountObj.value}p)
                    </button>
                    {activeDropdown === 'count' && (
                        <div className="absolute top-full mt-2 left-0 w-32 bg-[#1a1a1a]/90 backdrop-blur-xl border border-zinc-700 rounded-xl shadow-2xl overflow-hidden z-50 animate-in slide-in-from-top-2 fade-in duration-200">
                            {LENGTH_OPTIONS.map(opt => (
                                <button key={opt.id} onClick={() => { setSlideCountObj(opt); setActiveDropdown('none'); }} className={`w-full text-left px-4 py-3 text-xs hover:bg-purple-900/30 hover:text-purple-400 transition-colors flex justify-between ${slideCountObj.id === opt.id ? "text-purple-400 font-bold" : "text-gray-400"}`}>
                                    <span>{opt.label}</span>
                                    <span className="opacity-50">{opt.range}</span>
                                </button>
                            ))}
                        </div>
                    )}
                </div>

                <div className="relative dropdown-container">
                    <button onClick={() => setActiveDropdown(activeDropdown === 'theme' ? 'none' : 'theme')} className={`flex items-center gap-2 px-4 py-2 rounded-full border text-xs font-bold transition-all backdrop-blur-md ${activeDropdown === 'theme' ? "bg-purple-600 text-white border-purple-500 shadow-[0_0_15px_rgba(168,85,247,0.5)]" : "bg-white/5 text-gray-300 border-white/10 hover:bg-white/10"}`}>
                        <span>{t.emoji}</span> {t.name}
                    </button>
                    {activeDropdown === 'theme' && (
                        <div className="absolute top-full mt-2 left-0 w-48 bg-[#1a1a1a]/90 backdrop-blur-xl border border-zinc-700 rounded-xl shadow-2xl overflow-hidden z-50 animate-in slide-in-from-top-2 fade-in duration-200">
                            {Object.values(THEMES).map(theme => (
                                <button key={theme.id} onClick={() => { setCurrentTheme(theme.id as any); setActiveDropdown('none'); }} className={`w-full text-left px-4 py-3 text-xs hover:bg-purple-900/30 hover:text-purple-400 transition-colors flex items-center gap-2 ${currentTheme === theme.id ? "text-purple-400 font-bold bg-purple-900/10" : "text-gray-400"}`}>
                                    <span className="text-base">{theme.emoji}</span> {theme.name}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
             </div>

             <div className="relative group">
                 <div className={`absolute -inset-1 bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 rounded-2xl blur opacity-30 transition duration-1000 ${isGenerating ? "animate-pulse opacity-100" : "animate-pulse"}`}></div>
                 <div className="relative bg-[#111] rounded-2xl flex items-center p-2 border border-zinc-800 shadow-2xl h-[72px]">
                    {isGenerating ? (
                        <div className="flex-1 flex items-center justify-center gap-3 text-purple-400 font-mono animate-pulse">
                            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                            <span>{loadingText}</span>
                        </div>
                    ) : (
                        <>
                            <input type="text" value={inputValue} onChange={(e) => setInputValue(e.target.value)} onKeyDown={(e) => e.key === "Enter" && handleGenerateOutline()} placeholder="e.g., Teaching a dog how to code..." className="flex-1 bg-transparent text-white px-4 py-4 outline-none text-lg placeholder-zinc-600 font-mono" autoFocus />
                            <button onClick={handleGenerateOutline} className="bg-white text-black px-6 py-3 rounded-xl font-bold hover:bg-gray-200 transition-all whitespace-nowrap ml-2 shadow-lg">Generate</button>
                        </>
                    )}
                 </div>
             </div>
          </div>
        </div>
      )}

      {/* --- STEP 2: Review Outline --- */}
      {step === 'outline' && pptData && (
        <div className="relative z-10 w-full max-w-5xl animate-in slide-in-from-bottom-10 duration-700">
            <div className="mb-8 flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white mb-2">Review Outline</h2>
                    <div className="flex gap-3 text-xs font-mono text-gray-500">
                        <span className="bg-purple-900/30 text-purple-400 px-2 py-1 rounded border border-purple-500/30">{THEMES[currentTheme].name}</span>
                        <span className="bg-zinc-800 text-gray-400 px-2 py-1 rounded border border-zinc-700">{pptData.slides.length} Slides</span>
                    </div>
                </div>
            </div>
            <div className="space-y-4 mb-10">
                {pptData.slides.map((item: any, i: number) => (
                    <div key={i} className="bg-zinc-900/60 border border-zinc-800 p-6 rounded-xl flex gap-6 hover:border-zinc-600 transition-colors group backdrop-blur-sm items-start">
                        <div className="w-10 h-10 shrink-0 bg-zinc-800 rounded-lg flex items-center justify-center text-gray-400 font-mono text-sm font-bold group-hover:bg-purple-600 group-hover:text-white transition-colors mt-1">
                            {i + 1}
                        </div>
                        <div className="flex-1">
                            <div className="text-lg text-white font-bold mb-3">{item.title}</div>
                            {item.content?.bullet_points && (
                                <ul className="space-y-2">
                                    {item.content.bullet_points.map((pt: string, idx: number) => (
                                        <li key={idx} className="text-sm text-gray-400 flex gap-2"><span className="text-purple-500">•</span> {pt}</li>
                                    ))}
                                </ul>
                            )}
                            {item.visual?.need_image && (
                                <div className="mt-2 text-xs text-blue-400 bg-blue-900/20 px-2 py-1 rounded w-fit">Image: "{item.visual.image_prompt}"</div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
            <div className="flex justify-center pb-8 gap-4">
                <button onClick={() => setStep('input')} className="px-8 py-4 rounded-full font-bold text-gray-500 hover:text-white transition-colors">Back</button>
                <button onClick={handleRenderAndDownload} disabled={isGenerating} className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-16 py-4 rounded-full font-bold text-xl shadow-[0_0_40px_rgba(168,85,247,0.4)] hover:shadow-[0_0_60px_rgba(168,85,247,0.6)] hover:scale-[1.02] transition-all flex items-center gap-2">
                    {isGenerating ? "Rendering..." : "✨ Confirm & Preview"}
                </button>
            </div>
        </div>
      )}

      {/* --- STEP 3: Preview --- */}
      {step === 'preview' && (
        <div className="relative z-10 w-full max-w-6xl animate-in fade-in duration-1000">
            <div className="flex items-center mb-8 px-4 border-b border-white/10 pb-6">
                <h2 className="text-3xl font-bold text-white">🎉 Generation Result(For reference only)</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pb-10">
              {pptData.slides.map((slide: any, index: number) => (
                <div key={index} className="shadow-2xl rounded-xl perspective-1000">
                   <RenderSlide slide={slide} index={index} themeKey={currentTheme} />
                </div>
              ))}
            </div>
            <div className="flex justify-center pb-16 pt-6 gap-6 border-t border-white/10">
                  <button onClick={() => setStep('input')} className="px-8 py-4 rounded-full font-bold text-gray-500 hover:text-white transition-colors border border-zinc-800 hover:border-zinc-600 hover:bg-zinc-900">Create Another</button>
                  <button onClick={() => window.open(downloadUrl)} className="bg-green-600 text-white px-12 py-4 rounded-full font-bold text-lg hover:bg-green-500 shadow-xl flex items-center gap-3 transform hover:-translate-y-1 transition-all">Download .PPTX</button>
            </div>
        </div>
      )}
    </main>
  );
}