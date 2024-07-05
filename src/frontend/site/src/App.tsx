import React, { useState, useEffect } from "react";
import axios from "axios";
import './App.css';

// データの型を定義
interface CompatibilityData {
  compatibility: number;
  message: string;
}

// カウントアップアニメーション用のカスタムフック
const useCountUp = (end: number, duration: number = 1000) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTime: number | null = null;
    const animateCount = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = timestamp - startTime;
      const percentage = Math.min(progress / duration, 1);
      setCount(Math.floor(end * percentage));
      if (percentage < 1) {
        requestAnimationFrame(animateCount);
      }
    };
    requestAnimationFrame(animateCount);
  }, [end, duration]);

  return count;
};

function App() {
  const [data, setData] = useState<CompatibilityData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const url = "http://127.0.0.1:3001";

  const GetData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get<CompatibilityData>(url);
      setData(response.data);
    } catch (err) {
      setError("データの取得に失敗しました。");
      console.error("Error fetching data:", err);
    } finally {
      setLoading(false);
    }
  };

  const countUpScore = useCountUp(data?.compatibility ?? 0);

  return (
    <div className="app-container">
      <h1>相性診断テスト</h1>
      {loading ? (
        <p className="loading">読み込み中...</p>
      ) : error ? (
        <p className="error-message">{error}</p>
      ) : data ? (
        <div className="result">
          <h2>診断結果</h2>
          <p className="compatibility-score">あなたたちの相性は...</p>
          <h3 className="compatibility-score-2">{countUpScore}</h3>
          <p className="compatibility-score">GPT先生からのアドバイス</p>
          <p>{data.message}</p>
        </div>
      ) : (
        <button onClick={GetData}>診断を開始</button>
      )}
    </div>
  );
}

export default App;