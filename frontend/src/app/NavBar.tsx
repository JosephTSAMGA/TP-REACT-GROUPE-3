// =============================================================
// PARTIE 1/4 — Navigation & formulaire
// Fichiers de cette partie : App.tsx, StartScreen.tsx (+.css), NavBar.tsx (+.css).
// =============================================================
import { NavLink } from "react-router-dom";
import "./NavBar.css";

// Barre de navigation commune à toutes les pages, pour garder un style
// cohérent et permettre de vraiment naviguer entre les pages (au lieu
// d'un simple affichage conditionnel dans un seul composant).
export default function NavBar() {
  return (
    <nav className="nav-bar">
      <span className="nav-brand">GetClose</span>
      <div className="nav-links">
        {/* NavLink ajoute automatiquement la classe "active" sur le lien
            de la page actuellement affichée. */}
        <NavLink to="/" end className="nav-link">
          Accueil
        </NavLink>
        <NavLink to="/historique" className="nav-link">
          Historique
        </NavLink>
      </div>
    </nav>
  );
}
