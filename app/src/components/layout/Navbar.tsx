import React from "react";
import styles from "./layout.module.css";
import Link from "next/link";

export function Navbar() {
    return (
        <header className={styles.navbar}>
            <Link href="/" className={styles.navBrand}>
                Mailer Agent
            </Link>
            <div className={styles.navActions}>
                <button aria-label="Notifications">🔔</button>
                <div style={{ width: 32, height: 32, borderRadius: "50%", background: "var(--accent-muted)", color: "white", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14 }}>
                    U
                </div>
            </div>
        </header>
    );
}
