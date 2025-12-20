import { useState, useEffect } from "react";
import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";

export default function GlobalSearch() {
  const [open, setOpen] = useState(false);

  // Gestion du raccourci clavier (Cmd+K ou Ctrl+K)
  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  return (
    <>
      <Button
        variant="outline"
        className="relative h-9 w-64 justify-start text-sm text-muted-foreground font-normal bg-muted/50 hover:bg-muted border-none ring-1 ring-border shadow-sm transition-all hover:ring-primary/50"
        onClick={() => setOpen(true)}
      >
        <Search className="mr-2 h-4 w-4 text-muted-foreground" />
        <span>Rechercher...</span>
        <kbd className="pointer-events-none absolute right-1.5 top-1.5 hidden h-6 select-none items-center gap-1 rounded border bg-background px-1.5 font-mono text-[10px] font-medium opacity-100 sm:flex">
          <span className="text-xs">⌘</span>K
        </kbd>
      </Button>

      <CommandDialog open={open} onOpenChange={setOpen}>
        <CommandInput placeholder="Tapez votre recherche..." />
        <CommandList>
          <CommandEmpty>Aucun résultat trouvé.</CommandEmpty>
          <CommandGroup heading="Actions rapides">
            <CommandItem>Consulter les opportunités</CommandItem>
            <CommandItem>Voir les messages</CommandItem>
            <CommandItem>Paramètres du profil</CommandItem>
          </CommandGroup>
        </CommandList>
      </CommandDialog>
    </>
  );
}
