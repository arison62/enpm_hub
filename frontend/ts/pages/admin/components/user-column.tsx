import type { ColumnDef } from "@tanstack/react-table";

import { Checkbox } from "@/components/ui/checkbox";

import { roles_systeme, roles, statuses } from "../data/user";
import type { UserComplete } from "@/types/user";

import { DataTableColumnHeader } from "./data-table-column-header";
import { DataTableRowActions } from "./user-table-row-actions";

export const columns: ColumnDef<UserComplete>[] = [
  {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate")
        }
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
        className="translate-y-[2px]"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
        className="translate-y-[2px]"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "email",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Email" />
    ),
    cell: ({ row }) => <div className="w-[80px]">{row.getValue("email")}</div>,
    enableSorting: false,
    enableHiding: false,
  },
  {
    id: "nom_complet",
    accessorFn: (row) => row.profil.nom_complet,
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Nom" />
    ),
    cell: ({ row }) => (
      <div className="w-[80px]">{row.getValue("nom_complet")}</div>
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "role",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Role" />
    ),
    cell: ({ row }) => {
      const role = roles.find(
        (role) => role.value === row.getValue("role")
      );

      if (!role) {
        return null;
      }

      return (
        <div className="flex w-[100px] items-center">
          <span>{role.label}</span>
        </div>
      );
    },
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id));
    },
  },
  {
    accessorKey: "role_systeme",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Niveau acces" />
    ),
    cell: ({ row }) => {
      const role = roles_systeme.find(
        (role) => role.value === row.getValue("role_systeme")
      );

      if (!role) {
        return null;
      }

      return (
        <div className="flex w-[100px] items-center">
          <span>{role.label}</span>
        </div>
      )
    }
  },
  {
    accessorKey: "est_actif",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Status" />
    ),
    cell: ({ row }) => {
      const status = statuses.find(
        (status) => status.value === row.getValue("est_actif")
      );

      if (!status) {
        return null;
      }

      return (
        <div className="flex items-center">

          <span>{status.label}</span>
        </div>
      );
    },
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id));
    },
  },
  {
    id: "actions",
    cell: ({ row }) => <DataTableRowActions row={row} />,
  },
];
