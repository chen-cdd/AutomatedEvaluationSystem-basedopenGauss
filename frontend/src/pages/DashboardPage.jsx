import { useEffect, useState } from "react";
import { getJson } from "../api/client";
import StatCard from "../components/StatCard";
import SectionCard from "../components/SectionCard";

export default function DashboardPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getJson("/dashboard/overview").then(setData).catch(console.error);
  }, []);

  if (!data) {
    return <div className="page"><p>正在加载总览数据...</p></div>;
  }

  return (
    <div className="page">
      <div className="hero">
        <div>
          <p className="eyebrow">Agentic AI Evaluation</p>
          <h2>让日志变成可追踪、可解释、可对比的评测结果</h2>
        </div>
        <div className="hero-badge">openGauss + FastAPI + React</div>
      </div>

      <div className="stats-grid">
        <StatCard label="任务总数" value={data.stats.total_tasks} detail="已录入评测任务" />
        <StatCard label="完成任务" value={data.stats.completed_tasks} detail="已完成解析与评分" />
        <StatCard label="失败任务" value={data.stats.failed_tasks} detail="需要人工排查" />
        <StatCard label="平均分" value={data.stats.average_score} detail="全局综合评分" />
      </div>

      <div className="two-column">
        <SectionCard title="能力雷达视图">
          <div className="radar-list">
            {data.radar.map((item) => (
              <div key={item.label} className="radar-row">
                <span>{item.label}</span>
                <div className="meter">
                  <div style={{ width: `${item.value}%` }} />
                </div>
                <strong>{item.value}</strong>
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="模型对比">
          <div className="list">
            {data.model_comparison.map((item) => (
              <div key={item.model_name} className="list-row">
                <span>{item.model_name}</span>
                <span>{item.task_count} 个任务</span>
                <strong>{item.average_score}</strong>
              </div>
            ))}
          </div>
        </SectionCard>
      </div>

      <SectionCard title="低分案例">
        <div className="list">
          {data.bad_cases.length === 0 ? <p>暂无低分案例。</p> : data.bad_cases.map((item) => (
            <div key={item.task_id} className="list-row">
              <span>{item.task_name}</span>
              <span>{item.summary}</span>
              <strong>{item.total_score}</strong>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
