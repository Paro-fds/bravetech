import React from 'react';
import { GraduationCap, MapPin, Mail, Phone } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-900 text-slate-300 pt-16 pb-12 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">
          {/* Col 1 : Info */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white">
                <GraduationCap className="w-5 h-5" />
              </div>
              <span className="font-extrabold text-xl text-white tracking-tight">
                FDS PORTAIL
              </span>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed max-w-md mb-6">
              Plateforme numérique officielle de la Faculté des Sciences de l'Université d'État d'Haïti. Consultation des maquettes pédagogiques et dépôt dématérialisé des dossiers d'admission.
            </p>
            <div className="flex flex-col gap-2 text-xs text-slate-400">
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-blue-400 shrink-0" />
                <span>Angle Rues Mgr Guilloux et Joseph Janvier, Port-au-Prince, Haïti</span>
              </div>
              <div className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-blue-400 shrink-0" />
                <span>admission@fds.ueh.edu.ht</span>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="w-4 h-4 text-blue-400 shrink-0" />
                <span>+509 22 22 10 24</span>
              </div>
            </div>
          </div>

          {/* Col 2 : Cursus */}
          <div>
            <h4 className="text-white font-semibold text-sm tracking-wider uppercase mb-4">
              Départements
            </h4>
            <ul className="space-y-2.5 text-sm text-slate-400">
              <li><a href="#catalogue" className="hover:text-white transition-colors">Tronc Commun MPC</a></li>
              <li><a href="#catalogue" className="hover:text-white transition-colors">Génie Civil</a></li>
              <li><a href="#catalogue" className="hover:text-white transition-colors">Génie Électronique</a></li>
              <li><a href="#catalogue" className="hover:text-white transition-colors">Génie Électromécanique</a></li>
              <li><a href="#catalogue" className="hover:text-white transition-colors">Département d'Architecture</a></li>
            </ul>
          </div>

          {/* Col 3 : Accès rapide */}
          <div>
            <h4 className="text-white font-semibold text-sm tracking-wider uppercase mb-4">
              Informations
            </h4>
            <ul className="space-y-2.5 text-sm text-slate-400">
              <li><a href="#processus" className="hover:text-white transition-colors">Guide du candidat</a></li>
              <li><a href="#admission" className="hover:text-white transition-colors">Calendrier du concours</a></li>
              <li><a href="#pieces" className="hover:text-white transition-colors">Pièces justificatives requises</a></li>
              <li><span className="text-slate-500">Espace Administration (JWT)</span></li>
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-slate-800 text-xs text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p>© {new Date().getFullYear()} Faculté des Sciences — UEH. Tous droits réservés.</p>
          <p className="flex items-center gap-1">
            Bravetech · Projet de Génie Logiciel
          </p>
        </div>
      </div>
    </footer>
  );
};
