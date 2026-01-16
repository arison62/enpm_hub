import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface FormSectionProps {
  title: string;
  icon: ReactNode;
  children: ReactNode;
  className?: string;
}

export const FormSection = ({
  title,
  icon,
  children,
  className,
}: FormSectionProps) => {
  return (
    <div
      className={cn(
        "p-6 md:p-8 border-b border-border last:border-0",
        className
      )}
    >
      <h3 className="text-lg font-bold tracking-tight mb-6 flex items-center gap-2">
        <span className="text-primary">{icon}</span>
        {title}
      </h3>
      <div className="space-y-6">{children}</div>
    </div>
  );
};
