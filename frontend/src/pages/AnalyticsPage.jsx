import { useEffect, useState } from "react";
import { getJson } from "../api/client";
import SectionCard from "../components/SectionCard";

export default function AnalyticsPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getJson("/dashboard/overview").then(setData).catch(console.error);
  }, []);

  if (!data) {
    return <div className="page"><p>正在加载统计分析...</p></div>;
  }

  return (
    <div className="page">
      <div className="two-column">
        <SectionCard title="得分分布">
          <div className="bar-list">
            {data.radar.map((item) => (
              <div key={item.label} className="bar-item">
                <span>{item.label}</span>
                <div className="bar"><div style={{ width: `${item.value}%` }} /></div>
              </div>
            ))}
          </div>
        </SectionCard>
        <SectionCard title="模型横向对比">
          <div className="list">
            {data.model_comparison.map((item) => (
              <div className="list-row" key={item.model_name}>
                <span>{item.model_name}</span>
                <span>{item.task_count} 个任务</span>
                <strong>{item.average_score}</strong>
              </div>
            ))}
          </div>
        </SectionCard>
      </div>
      <SectionCard title="运行指标">
        <div className="score-grid">
          <div><span>平均耗时</span><strong>{data.stats.average_processing_seconds}s</strong></div>
          <div><span>平均 Token</span><strong>{data.stats.average_tokens}</strong></div>
          <div><span>平均分</span><strong>{data.stats.average_score}</strong></div>
          <div><span>完成任务</span><strong>{data.stats.completed_tasks}</strong></div>
        </div>
      </SectionCard>
    </div>
  );
}
