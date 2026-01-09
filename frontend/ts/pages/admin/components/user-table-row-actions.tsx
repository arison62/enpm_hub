import { type Row } from "@tanstack/react-table";
import { MoreHorizontal } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import type { UserComplete } from "@/types/user";
import type { AxiosError } from "axios";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useUserActions } from "@/api/users";

interface DataTableRowActionsProps<TData> {
  row: Row<TData>;
}

export function DataTableRowActions<TData>({
  row,
}: DataTableRowActionsProps<TData>) {
  const {removeUser, toggleStatus} = useUserActions();
  const user = row.original as UserComplete;
  const slug = user.profil.slug;
  const est_actif = user.est_actif;

  const handleToggleStatus = async () => {
    try {
      await toggleStatus.mutateAsync({
        userId: user.id,
        est_actif: !est_actif,
      });
    } catch (error) {
      console.log(error);
      const axiosError = error as AxiosError<{detail: string }>;
      toast.error(
        axiosError.response?.data?.detail ||
          "Impossible de modifier le statut de l'utilisateur."
      )
    }
  };
  const handleDelete = async () => {
    try {
      await removeUser.mutateAsync(user.id);
    } catch (error) {
      const axiosError = error as AxiosError<{ detail: string }>;
      toast.error(
        axiosError.response?.data?.detail||
          "Impossible de supprimer l'utilisateur."
      );
    }
  };
  

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          className="flex h-8 w-8 p-0 data-[state=open]:bg-muted"
        >
          <MoreHorizontal />
          <span className="sr-only">Open menu</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-[160px]">
        <Dialog>
          <DialogTrigger asChild>
            <DropdownMenuItem
              onSelect={(e) => e.preventDefault()} // ← Clé de la correction !
            >
              Voir le profil
            </DropdownMenuItem>
          </DialogTrigger>
          <DialogContent className="max-w-6xl h-[90vh] p-0">
            <DialogTitle className="sr-only">Profil utilisateur</DialogTitle>
            <iframe
              src={`/profile/${slug}`}
              className="w-full h-full border-0 rounded-lg"
              title="Profil utilisateur"
              loading="lazy"
              sandbox="allow-scripts allow-same-origin allow-popups"
            />
          </DialogContent>
        </Dialog>
        <DropdownMenuItem onClick={handleToggleStatus}>
          {est_actif ? "Desactiver" : "Activer"}
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem className="text-red-600" onClick={handleDelete}>
          Supprimer
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
