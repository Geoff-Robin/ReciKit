import React, { useState } from "react";
import {
  Facebook,
  Twitter,
  Instagram,
  Linkedin,
  Mail,
  Phone,
  MapPin,
} from "lucide-react";

const Footer = () => {
  const [email, setEmail] = useState("");

  const handleSubscribe = () => {
    if (email) {
      alert(`Thank you for subscribing with ${email}!`);
      setEmail("");
    }
  };

  return (
    <footer className="bg-gradient-to-r from-green-700 via-emerald-700 to-green-800 text-white py-8">
      <div className="max-w-6xl mx-auto px-6">
        <div className="grid md:grid-cols-3 gap-6 items-start">

          {/* Brand Info */}
          <div className="space-y-3">
            <h3 className="text-xl font-bold">Ricket</h3>
            <p className="text-green-50 text-sm leading-relaxed">
              Your smart kitchen companion for healthier eating and smarter meal
              planning.
            </p>
            <div className="flex space-x-3 pt-2">
              {[Facebook, Twitter, Instagram, Linkedin].map((Icon, i) => (
                <button
                  key={i}
                  className="w-8 h-8 bg-white/20 hover:bg-white/30 rounded-full flex items-center justify-center transition"
                >
                  <Icon className="w-4 h-4" />
                </button>
              ))}
            </div>
          </div>

          {/* Contact */}
          <div className="space-y-3">
            <h4 className="text-lg font-semibold">Get in Touch</h4>
            <div className="space-y-2">
              <div className="flex items-center space-x-2 text-green-50">
                <Phone className="w-4 h-4" />
                <span className="text-sm">+1 (234) 567-890</span>
              </div>
              <div className="flex items-center space-x-2 text-green-50">
                <Mail className="w-4 h-4" />
                <span className="text-sm">hello@ricket.com</span>
              </div>
              <div className="flex items-start space-x-2 text-green-50">
                <MapPin className="w-4 h-4 mt-0.5" />
                <span className="text-sm">
                  123 Kitchen Street, Food City, FC 12345
                </span>
              </div>
            </div>
          </div>

          {/* Newsletter */}
          <div className="space-y-3">
            <h4 className="text-lg font-semibold">Stay Updated</h4>
            <p className="text-green-50 text-sm">
              Get recipes and meal tips weekly.
            </p>
            <div className="flex space-x-2">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email address"
                className="flex-1 px-3 py-2 rounded-full bg-white/20 border border-white/30 text-white placeholder-green-100 focus:ring-2 focus:ring-white/40 text-sm outline-none"
              />
              <button
                onClick={handleSubscribe}
                className="px-5 py-2 bg-white text-green-700 font-semibold rounded-full hover:bg-green-50 transition-all text-sm"
              >
                Join
              </button>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-white/20 mt-6 pt-4 flex flex-col md:flex-row justify-between items-center text-sm text-green-50 space-y-2 md:space-y-0">
          <p>© 2025 Ricket. All rights reserved.</p>
          <div className="flex space-x-4">
            <button className="hover:text-white transition">Privacy</button>
            <button className="hover:text-white transition">Terms</button>
            <button className="hover:text-white transition">Cookies</button>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
