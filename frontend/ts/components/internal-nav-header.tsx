import { ChevronLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { useInternalNav } from "@/contexts/internal-nav-context";
import React from "react";

export const NavHeader = () => {
  const { stack, pop, goToIndex } = useInternalNav();
  const isRoot = stack.length === 1;
  const currentItem = stack[stack.length - 1];

  return (
    <>
      {stack.length > 1 && (
        <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container flex h-14 items-center px-4">
            {/* MOBILE : Bouton Retour */}
            <div className="flex lg:hidden items-center gap-2">
              {!isRoot && (
                <Button variant="ghost" size="icon" onClick={pop}>
                  <ChevronLeft className="size-5" />
                </Button>
              )}
              <h1 className="font-semibold text-sm truncate max-w-[200px]">
                {currentItem.title}
              </h1>
            </div>

            {/* DESKTOP : Breadcrumbs */}
            <div className="hidden lg:flex items-center w-full">
              <Breadcrumb>
                <BreadcrumbList>
                  {stack.map((item, index) => (
                    <React.Fragment key={item.id}>
                      {index >= 1 && <BreadcrumbSeparator />}
                      <BreadcrumbItem>
                        {index === stack.length - 1 ? (
                          <BreadcrumbPage>{item.title}</BreadcrumbPage>
                        ) : (
                          <BreadcrumbLink
                            className="cursor-pointer"
                            onClick={() => goToIndex(index)}
                          >
                            {item.title}
                          </BreadcrumbLink>
                        )}
                      </BreadcrumbItem>
                    </React.Fragment>
                  ))}
                </BreadcrumbList>
              </Breadcrumb>
            </div>
          </div>
        </header>
      )}
    </>
  );
};
