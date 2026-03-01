import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
});

export const metadata: Metadata = {
  title: "Mailer Agent",
  description: "Collaborative email management with AI drafting",
};

import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";
import styles from "@/components/layout/layout.module.css";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${jetbrainsMono.variable}`}>
        <div className={styles.appShell}>
          <Navbar />
          <div className={styles.mainContainer}>
            <Sidebar />
            <main className={styles.contentArea}>
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
