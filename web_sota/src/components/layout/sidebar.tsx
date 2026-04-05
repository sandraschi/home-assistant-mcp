import { Link, useLocation } from 'react-router-dom';
import { cn } from '@/common/utils';
import {
    LayoutDashboard,
    Bot,
    Settings,
    ChevronLeft,
    ChevronRight,
    Home,
    Activity,
    Wrench,
    Grid,
    HelpCircle,
    Lightbulb,
    Thermometer,
    ShieldCheck
} from 'lucide-react';

interface SidebarProps {
    collapsed: boolean;
    onToggle: () => void;
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
    const location = useLocation();

    const navItems = [
        { href: '/', label: 'Overview', icon: LayoutDashboard },
        { href: '/entities', label: 'Entities', icon: Grid },
        { href: '/automations', label: 'Automations', icon: Activity },
        { href: '/tools', label: 'Tools', icon: Wrench },
        { href: '/apps', label: 'App Hub', icon: Grid },
        { href: '/chat', label: 'HA Command', icon: Bot },
        { href: '/status', label: 'Status', icon: Activity },
        { href: '/settings', label: 'Settings', icon: Settings },
        { href: '/help', label: 'Help', icon: HelpCircle },
    ];

    return (
        <aside
            className={cn(
                "glass-sidebar relative flex flex-col transition-all duration-300 ease-in-out",
                collapsed ? "w-20" : "w-64"
            )}
        >
            <div className="flex h-20 items-center px-6">
                <div className="flex items-center gap-3 font-bold text-slate-100">
                    <div className="w-8 h-8 rounded-lg bg-orange-600 flex items-center justify-center orange-glow">
                        <Home className="h-5 w-5 text-white" />
                    </div>
                    {!collapsed && <span className="text-lg font-bold gradient-text text-orange-200/90">HA-MCP</span>}
                </div>
            </div>

            <nav className="flex-1 space-y-1 p-3">
                {navItems.map((item) => {
                    const isActive = location.pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            to={item.href}
                            className={cn(
                                "nav-item",
                                isActive && "active",
                                collapsed ? "justify-center" : "justify-start"
                            )}
                        >
                            <item.icon className={cn("h-5 w-5", isActive && "text-orange-400")} />
                            {!collapsed && <span>{item.label}</span>}

                            {collapsed && (
                                <div className="absolute left-full ml-4 hidden rounded-lg bg-black/80 backdrop-blur-md px-3 py-1.5 text-xs text-white group-hover:block z-50 whitespace-nowrap border border-white/10">
                                    {item.label}
                                </div>
                            )}
                        </Link>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-white/[0.06]">
                <button
                    onClick={onToggle}
                    className="flex w-full items-center justify-center rounded-xl p-2.5 text-slate-400 hover:text-white hover:bg-white/[0.05] transition-all"
                >
                    {collapsed ? <ChevronRight className="h-5 w-5" /> : <div className="flex items-center w-full"><ChevronLeft className="h-5 w-5 mr-3" /><span>Collapse Sidebar</span></div>}
                </button>
            </div>
        </aside>
    );
}
