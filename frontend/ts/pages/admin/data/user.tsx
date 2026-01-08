import {
  ArrowDown,
  ArrowRight,
  ArrowUp,
  PlayCircle,
  StopCircle,
} from "lucide-react";

export const roles =  [
  {
    value: "etudiant",
    label: "Etudiant",
  },
  {
    value: "enseignant",
    label: "Enseignant",
  },
  {
    value: "alumni",
    label: "Alumni",
  },{
    value: "personnel_admin",
    label: "Personnel Admin",
  },{
    value: "partenaire",
    label: "Partenaire",
  }
]

export const roles_systeme =  [
  {
    value: "super_admin",
    label: "Super Admin",
  },
  {
    value: "user",
    label: "Utilisateur",
  },
  {
    value: "admin_site",
    label: "Admin Site",
  }
]

export  const statuses = [
  {
    value: true,
    label: "Actif",
    icon: PlayCircle
  },{
    value: false,
    label: "Inactif",
    icon: StopCircle
  }
]

export const labels = [
  {
    value: "bug",
    label: "Bug",
  },
  {
    value: "feature",
    label: "Feature",
  },
  {
    value: "documentation",
    label: "Documentation",
  },
];

// export const statuses = [
//   {
//     value: "backlog",
//     label: "Backlog",
//     icon: HelpCircle,
//   },
//   {
//     value: "todo",
//     label: "Todo",
//     icon: Circle,
//   },
//   {
//     value: "in progress",
//     label: "In Progress",
//     icon: Timer,
//   },
//   {
//     value: "done",
//     label: "Done",
//     icon: CheckCircle,
//   },
//   {
//     value: "canceled",
//     label: "Canceled",
//     icon: CircleOff,
//   },
// ];

export const priorities = [
  {
    label: "Low",
    value: "low",
    icon: ArrowDown,
  },
  {
    label: "Medium",
    value: "medium",
    icon: ArrowRight,
  },
  {
    label: "High",
    value: "high",
    icon: ArrowUp,
  },
];
