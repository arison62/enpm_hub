import React, { useState } from "react";
import { Upload, UserPlus, Check, AlertCircle } from "lucide-react";
import * as XLSX from "xlsx";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { UserCreateAdmin } from "@/types/user";

interface ColumnMapping {
  [key: string]: string;
}

interface ImportedUser {
  [key: string]: string;
}


interface UserManagementDialogsProps {
  showCreateDialog: boolean;
  setShowCreateDialog: (show: boolean) => void;
  showImportDialog: boolean;
  setShowImportDialog: (show: boolean) => void;
  onUserCreated: () => void;
  onUsersImported: () => void;
}



const CreateUserForm = ({ onSubmit, onCancel }: any) => {
  const [formData, setFormData] = useState({
    email: "",
    telephone: "",
    nom_complet: "",
    role_systeme: "user",
    status_global: "etudiant",
  });

  const [errors, setErrors] = useState<any>({});

  const validateForm = () => {
    const newErrors: any = {};

    if (!formData.email && !formData.telephone) {
      newErrors.contact =
        "Au moins un email ou un numéro de téléphone est requis";
    }

    if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Email invalide";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validateForm()) {
      const userData: UserCreateAdmin = {
        email: formData.email,
        role_systeme: formData.role_systeme,
        profil: {
          nom_complet: formData.nom_complet,
          matricule: null,
          titre: null,
          statut_global: formData.status_global,
          annee_sortie: null,
          telephone: formData.telephone || null,
          domaine: null,
          bio: null,
          adresse: null,
        },
      };
      onSubmit(userData);
    }
  };

  return (
    <div className="space-y-4">
      {errors.contact && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{errors.contact}</AlertDescription>
        </Alert>
      )}

      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="exemple@email.com"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        />
        {errors.email && (
          <p className="text-sm text-destructive flex items-center gap-1">
            <AlertCircle className="h-4 w-4" />
            {errors.email}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="telephone">Numéro de téléphone</Label>
        <Input
          id="telephone"
          type="tel"
          placeholder="+237 6XX XXX XXX"
          value={formData.telephone}
          onChange={(e) =>
            setFormData({ ...formData, telephone: e.target.value })
          }
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="nom">Nom complet (optionnel)</Label>
        <Input
          id="nom"
          type="text"
          placeholder="Aminatou Seidou"
          value={formData.nom_complet}
          onChange={(e) =>
            setFormData({ ...formData, nom_complet: e.target.value })
          }
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="role">Niveau d'accès</Label>
        <Select
          value={formData.role_systeme}
          onValueChange={(value) =>
            setFormData({ ...formData, role_systeme: value })
          }
        >
          <SelectTrigger id="role_syteme">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="user">Utilisateur</SelectItem>
            <SelectItem value="admin_site">Administrateur</SelectItem>
            <SelectItem value="super_admin">Modérateur</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div className="space-y-2">
        <Label htmlFor="role">Type compte</Label>
        <Select
          value={formData.role_systeme}
          onValueChange={(value) =>
            setFormData({ ...formData, status_global: value })
          }
        >
          <SelectTrigger id="status_global">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="etudiant">Edutiant</SelectItem>
            <SelectItem value="alumni">Alumni</SelectItem>
            <SelectItem value="enseignant">Enseignant</SelectItem>
            <SelectItem value="personnel_admin">
              Personnel d'administration
            </SelectItem>
            <SelectItem value="partenaire">
              Partenaire
            </SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="flex justify-end gap-2 pt-4">
        <Button type="button" variant="outline" onClick={onCancel}>
          Annuler
        </Button>
        <Button onClick={handleSubmit}>
          <UserPlus className="mr-2 h-4 w-4" />
          Créer l'utilisateur
        </Button>
      </div>
    </div>
  );
};

const ColumnMappingForm = ({ headers, onSubmit, onCancel }: any) => {
  const [mapping, setMapping] = useState<ColumnMapping>(() => {
    const initialMapping: ColumnMapping = {};
    headers.forEach((header: string) => {
      const normalized = header.toLowerCase().trim();
      if (normalized.includes("email")) initialMapping[header] = "email";
      else if (normalized.includes("tel") || normalized.includes("phone"))
        initialMapping[header] = "telephone";
      else if (normalized.includes("nom"))
        initialMapping[header] = "nom_complet";
      else initialMapping[header] = "ignore";
    });
    return initialMapping;
  });

  const handleMappingChange = (header: string, value: string) => {
    setMapping({ ...mapping, [header]: value });
  };

  return (
    <div className="space-y-4">
      <Alert>
        <AlertDescription>
          Associez chaque colonne du fichier à un attribut utilisateur. Les
          colonnes non mappées seront ignorées.
        </AlertDescription>
      </Alert>

      <div className="space-y-3">
        {headers.map((header: string) => (
          <div key={header} className="grid grid-cols-2 gap-4 items-center">
            <Label className="font-medium">{header}</Label>
            <Select
              value={mapping[header] || "ignore"}
              onValueChange={(value) => handleMappingChange(header, value)}
            >
              <SelectTrigger>
                <SelectValue placeholder="Ignorer" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ignore">Ignorer cette colonne</SelectItem>
                <SelectItem value="email">Email</SelectItem>
                <SelectItem value="telephone">Téléphone</SelectItem>
                <SelectItem value="nom_complet">Nom complet</SelectItem>
                <SelectItem value="role_systeme">Niveau d'accès</SelectItem>
                <SelectItem value="status_global">Type compte</SelectItem>
              </SelectContent>
            </Select>
          </div>
        ))}
      </div>

      <div className="flex justify-end gap-2 pt-4">
        <Button type="button" variant="outline" onClick={onCancel}>
          Annuler
        </Button>
        <Button onClick={() => onSubmit(mapping)}>
          <Check className="mr-2 h-4 w-4" />
          Confirmer le mapping
        </Button>
      </div>
    </div>
  );
};

const PreviewUsers = ({ users, onConfirm, onCancel }: any) => {
  const validUsers = users.filter((u: any) => u.email || u.telephone);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          {validUsers.length} utilisateur(s) valide(s) sur {users.length}
        </p>
      </div>

      {validUsers.length === 0 ? (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Aucun utilisateur valide trouvé. Assurez-vous que chaque ligne
            contient au moins un email ou un téléphone.
          </AlertDescription>
        </Alert>
      ) : (
        <div className="border rounded-lg overflow-scroll w-[480px]">
          <div className="max-h-96 overflow-y-auto">
            <Table>
              <TableHeader className="sticky top-0 bg-muted">
                <TableRow>
                  <TableHead>Email</TableHead>
                  <TableHead>Téléphone</TableHead>
                  <TableHead>Nom</TableHead>
                  <TableHead>Niveau d'accès</TableHead>
                  <TableHead>Type compte</TableHead>
                </TableRow>
              </TableHeader>

              <TableBody>
                {validUsers.map((user: any, index: number) => (
                  <TableRow key={index}>
                    <TableCell>{user.email || "-"}</TableCell>
                    <TableCell>{user.telephone || "-"}</TableCell>
                    <TableCell>{user.nom_complet || "-"}</TableCell>
                    <TableCell>{user.role_systeme || "-"}</TableCell>
                    <TableCell>{user.status_global || "-"}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </div>
      )}

      <div className="flex justify-end gap-2 pt-4">
        <Button type="button" variant="outline" onClick={onCancel}>
          Annuler
        </Button>
        <Button
          onClick={() => onConfirm(validUsers)}
          disabled={validUsers.length === 0}
        >
          <Check className="mr-2 h-4 w-4" />
          Importer {validUsers.length} utilisateur(s)
        </Button>
      </div>
    </div>
  );
};

const FileUploadArea = ({ onFileSelect }: any) => {
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <div className="space-y-4">
      <Alert>
        <AlertDescription>
          Sélectionnez un fichier Excel (.xlsx, .xls) ou CSV contenant les
          données utilisateurs.
        </AlertDescription>
      </Alert>
      <div className="border-2 border-dashed rounded-lg p-12 text-center hover:border-muted-foreground/50 transition-colors">
        <input
          type="file"
          accept=".xlsx,.xls,.csv"
          onChange={handleFileChange}
          className="hidden"
          id="file-upload"
        />
        <label htmlFor="file-upload" className="cursor-pointer block">
          <Upload className="mx-auto h-12 w-12 text-muted-foreground" />
          <p className="mt-4 text-sm font-medium">
            Cliquez pour sélectionner un fichier
          </p>
          <p className="mt-2 text-xs text-muted-foreground">
            Excel (.xlsx, .xls) ou CSV
          </p>
        </label>
      </div>
    </div>
  );
};

export const UserManagementDialogs: React.FC<UserManagementDialogsProps> = ({
  showCreateDialog,
  setShowCreateDialog,
  showImportDialog,
  setShowImportDialog,
  onUserCreated,
  onUsersImported,
}) => {
  const [importStep, setImportStep] = useState<
    "upload" | "mapping" | "preview"
  >("upload");
  const [fileHeaders, setFileHeaders] = useState<string[]>([]);
  const [importedData, setImportedData] = useState<ImportedUser[]>([]);
  const [mappedUsers, setMappedUsers] = useState<any[]>([]);

  const handleFileSelect = (file: File) => {
    const reader = new FileReader();
    reader.onload = (event) => {
      const data = event.target?.result;
      const workbook = XLSX.read(data, { type: "binary" });
      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];
      const jsonData = XLSX.utils.sheet_to_json(sheet);

      if (jsonData.length > 0) {
        const headers = Object.keys(jsonData[0] as object);
        setFileHeaders(headers);
        setImportedData(jsonData as ImportedUser[]);
        setImportStep("mapping");
      }
    };
    // reader.readAsBinaryString(file);
    reader.readAsArrayBuffer(file)
  };

  const handleMappingSubmit = (mapping: ColumnMapping) => {
    const users = importedData.map((row) => {
      const user: any = {
        email: "",
        telephone: "",
        nom_complet: "",
        role_systeme: "utilisateur",
      };

      Object.entries(mapping).forEach(([header, attribute]) => {
        if (attribute && attribute !== "ignore" && row[header]) {
          user[attribute] = String(row[header]);
        }
      });

      return user;
    });

    setMappedUsers(users);
    setImportStep("preview");
  };

  const handleCreateUser = async (userData: UserCreateAdmin) => {
    try {
      // TODO: Remplacer par votre appel API
      // await createUserAPI(userData);
      console.log("Creating user:", userData);
      onUserCreated();
    } catch (error) {
      console.error("Error creating user:", error);
    }
  };

  const handleImportUsers = async (users: any[]) => {
    try {
      // TODO: Remplacer par votre appel API
      // await bulkCreateUsersAPI(users);
      console.log("Importing users:", users);
      onUsersImported();
      resetImport();
    } catch (error) {
      console.error("Error importing users:", error);
    }
  };

  const resetImport = () => {
    setImportStep("upload");
    setFileHeaders([]);
    setImportedData([]);
    setMappedUsers([]);
  };

  const handleImportDialogClose = (open: boolean) => {
    setShowImportDialog(open);
    if (!open) {
      resetImport();
    }
  };

  return (
    <>
      {/* Create User Dialog */}
      <Dialog open={showCreateDialog} onOpenChange={setShowCreateDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Créer un nouvel utilisateur</DialogTitle>
          </DialogHeader>
          <CreateUserForm
            onSubmit={handleCreateUser}
            onCancel={() => setShowCreateDialog(false)}
          />
        </DialogContent>
      </Dialog>

      {/* Import Users Dialog */}
      <Dialog open={showImportDialog} onOpenChange={handleImportDialogClose}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>
              {importStep === "upload" && "Importer des utilisateurs"}
              {importStep === "mapping" && "Mapper les colonnes"}
              {importStep === "preview" && "Prévisualisation des utilisateurs"}
            </DialogTitle>
          </DialogHeader>

          {importStep === "upload" && (
            <FileUploadArea onFileSelect={handleFileSelect} />
          )}

          {importStep === "mapping" && (
            <ColumnMappingForm
              headers={fileHeaders}
              onSubmit={handleMappingSubmit}
              onCancel={() => handleImportDialogClose(false)}
            />
          )}

          {importStep === "preview" && (
            <PreviewUsers
              users={mappedUsers}
              onConfirm={handleImportUsers}
              onCancel={() => handleImportDialogClose(false)}
            />
          )}
        </DialogContent>
      </Dialog>
    </>
  );
};