import { type Table } from "@tanstack/react-table";
import { X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { DataTableViewOptions } from "./data-table-view-options";
import { DataTableFacetedFilter } from "./data-table-faceted-filter";


import type { LucideIcon } from "lucide-react";

export interface FacetedOption {
  label: string;
  value: string;
  icon?: LucideIcon;
}

export interface FacetedFilterConfig<TData> {
  columnId: keyof TData & string;
  title: string;
  options: FacetedOption[];
}

export interface SearchConfig<TData> {
  columnId: keyof TData & string | undefined;
  placeholder?: string;
}


interface DataTableToolbarProps<TData> {
  table: Table<TData>;
  search?: SearchConfig<TData>;
  filters?: FacetedFilterConfig<TData>[];
}

export function DataTableToolbar<TData>({
  table,
  search,
  filters = [],
}: DataTableToolbarProps<TData>) {
  const isFiltered = table.getState().columnFilters.length > 0;

  return (
    <div className="flex items-center justify-between">
      <div className="flex flex-1 items-center space-x-2">
        {/* Search */}
        {search && search.columnId && (
          <>
            {(() => {
              const column = table.getColumn(search.columnId);
              return column ? (
                <Input
                  placeholder={search.placeholder ?? "Search..."}
                  value={(column.getFilterValue() as string) ?? ""}
                  onChange={(e) => column.setFilterValue(e.target.value)}
                  className="h-8 w-[150px] lg:w-[250px]"
                />
              ) : null;
            })()}
          </>
        )}
        {/*  Faceted filters */}
        {filters.map((filter) => {
          const column = table.getColumn(filter.columnId);
          if (!column) return null;

          return (
            <DataTableFacetedFilter
              key={filter.columnId}
              column={column}
              title={filter.title}
              options={filter.options}
            />
          );
        })}

        {/*  Reset */}
        {isFiltered && (
          <Button
            variant="ghost"
            onClick={() => table.resetColumnFilters()}
            className="h-8 px-2 lg:px-3"
          >
            Reset
            <X className="ml-2 h-4 w-4" />
          </Button>
        )}
      </div>

      <DataTableViewOptions table={table} />
    </div>
  );
}