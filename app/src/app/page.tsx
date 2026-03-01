export default function Home() {
  return (
    <div>
      <h1 className="text-4xl font-bold">Welcome to Mailer Agent</h1>
      <p style={{ marginTop: "var(--space-md)", color: "var(--text-secondary)" }}>
        Collaborative email management with AI drafting and approval workflows.
      </p>

      <div style={{
        marginTop: "var(--space-xl)",
        padding: "var(--space-md)",
        borderRadius: "var(--radius-md)",
        background: "var(--bg-secondary)",
        border: "1px solid var(--border)",
        boxShadow: "var(--shadow-card)"
      }}>
        <h2>Dashboard Overview</h2>
        <p style={{ marginTop: "var(--space-sm)" }}>Select a group from the sidebar to get started.</p>
      </div>
    </div>
  );
}
