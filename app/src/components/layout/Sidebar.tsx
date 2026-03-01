import React from "react";
import styles from "./layout.module.css";
import Link from "next/link";

const items = [
    // TODO(Phase 2): Make hrefs dynamic using useParams() hook for active group context
    { label: "Dashboard", href: "/dashboard", icon: "📊" },
    { label: "Groups", href: "/groups/1", icon: "📁" }, /* mock link */
    { label: "Members", href: "/groups/1/members", icon: "👥" },
    { label: "Templates", href: "/groups/1/templates", icon: "📋" },
    { label: "Mails", href: "/groups/1/mails", icon: "✉️" },
    { label: "Notifications", href: "/groups/1/notifications", icon: "🔔" },
    { label: "Settings", href: "/groups/1/settings", icon: "⚙️" },
];

export function Sidebar() {
    return (
        <aside className={styles.sidebar}>
            <nav>
                {items.map((item) => (
                    <Link key={item.label} href={item.href} className={styles.sidebarItem}>
                        <span style={{ marginRight: "var(--space-sm)" }}>{item.icon}</span>
                        <span>{item.label}</span>
                    </Link>
                ))}
            </nav>
        </aside>
    );
}
