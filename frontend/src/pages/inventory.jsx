import React, { useState, useEffect, useCallback } from "react";
import { Plus, Trash2, Search, ShoppingBasket, ArrowLeft, Loader2, Edit2, Check, X } from "lucide-react";
import { Link } from "react-router-dom";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const Inventory = () => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [saving, setSaving] = useState(false);

    const [newItem, setNewItem] = useState("");
    const [newQuantity, setNewQuantity] = useState("");
    const [newUnit, setNewUnit] = useState("pcs");
    const [newItemCategory, setNewItemCategory] = useState("Pantry");
    const [searchQuery, setSearchQuery] = useState("");

    const [editingId, setEditingId] = useState(null);
    const [editQuantity, setEditQuantity] = useState("");
    const [editUnit, setEditUnit] = useState("");

    // Fetch Inventory
    const fetchInventory = useCallback(async () => {
        try {
            const res = await fetch(import.meta.env.VITE_BACKEND_URL + "/api/inventory", {
                method: "GET",
                credentials: "include",
            });
            if (!res.ok) throw new Error("Failed to load inventory");
            const data = await res.json();
            const normalizedData = (Array.isArray(data) ? data : []).map((item, index) => ({
                ...item,
                id: item.id || `item-${index}-${Date.now()}`,
                name: item.name || item.ingredient_name || "Unknown Item",
                category: item.category || "Pantry",
                quantity: item.quantity || "1",
                unit: item.unit || item.metric || ""
            }));
            setItems(normalizedData);
        } catch (err) {
            console.error(err);
            setError("Could not load inventory. Please try again.");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchInventory();
    }, [fetchInventory]);

    // Save Inventory
    const saveInventory = async (updatedItems) => {
        setSaving(true);
        try {
            setItems(updatedItems); // Optimistic update
            const res = await fetch(import.meta.env.VITE_BACKEND_URL + "/api/inventory", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify(updatedItems),
            });
            if (!res.ok) throw new Error("Failed to save changes");
        } catch (err) {
            console.error(err);
            setError("Failed to save changes. Please try again.");
            fetchInventory(); // Revert on error
        } finally {
            setSaving(false);
        }
    };

    const handleAddItem = async (e) => {
        e.preventDefault();
        if (!newItem.trim()) return;

        const item = {
            id: Date.now(),
            name: newItem,
            quantity: newQuantity || "1",
            unit: newUnit || "",
            category: newItemCategory,
        };

        await saveInventory([...items, item]);
        setNewItem("");
        setNewQuantity("");
        setNewUnit("");
    };

    const handleDeleteItem = async (id) => {
        const updated = items.filter((item) => item.id !== id);
        await saveInventory(updated);
    };

    const startEditing = (item) => {
        setEditingId(item.id);
        setEditQuantity(item.quantity);
        setEditUnit(item.unit || "");
    };

    const cancelEditing = () => {
        setEditingId(null);
        setEditQuantity("");
        setEditUnit("");
    };

    const saveEdit = async (id) => {
        const updated = items.map(item =>
            item.id === id ? { ...item, quantity: editQuantity, unit: editUnit } : item
        );
        await saveInventory(updated);
        setEditingId(null);
        setEditUnit("");
    };

    const filteredItems = items.filter((item) =>
        item.name && typeof item.name === 'string' && item.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const categories = ["Produce", "Dairy", "Meat", "Bakery", "Pantry", "Frozen", "Other"];
    const units = [
        "pcs", "kg", "g", "mg", "l", "ml", "cup", "tbsp", "tsp",
        "oz", "lb", "packet", "box", "can", "bottle", "jar", "slice"
    ];

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-900 flex items-center justify-center">
                <Loader2 className="w-10 h-10 text-emerald-500 animate-spin" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white p-4 md:p-8 font-sans">
            <div className="max-w-4xl mx-auto space-y-8">
                {/* Header */}
                <div className="flex items-center justify-between">
                    <Link to="/home" className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
                        <ArrowLeft className="w-5 h-5" />
                        <span>Back to Home</span>
                    </Link>
                    <div className="flex items-center gap-3">
                        <div className="p-3 bg-emerald-500/10 rounded-full">
                            <ShoppingBasket className="w-8 h-8 text-emerald-500" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold bg-gradient-to-r from-emerald-400 to-teal-500 bg-clip-text text-transparent">
                                My Inventory
                            </h1>
                            <p className="text-gray-400 text-sm">Manage your pantry essentials</p>
                        </div>
                    </div>
                </div>

                {error && (
                    <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-4 rounded-xl text-center">
                        {error}
                    </div>
                )}

                {/* Add Item Form */}
                <div className="bg-gray-800/50 backdrop-blur-xl border border-gray-700/50 rounded-2xl p-6 shadow-xl">
                    <h2 className="text-lg font-semibold mb-4 text-emerald-100 flex items-center gap-2">
                        <Plus className="w-5 h-5 text-emerald-500" />
                        Add New Item
                    </h2>
                    <form onSubmit={handleAddItem} className="grid grid-cols-1 md:grid-cols-12 gap-4">
                        <div className="md:col-span-4">
                            <Input
                                placeholder="Item Name (e.g., Rice)"
                                value={newItem}
                                onChange={(e) => setNewItem(e.target.value)}
                                className="bg-gray-900/50 border-gray-700 text-white placeholder:text-gray-500 focus-visible:ring-emerald-500/50"
                            />
                        </div>
                        <div className="md:col-span-2">
                            <Input
                                placeholder="Qty (e.g., 2)"
                                value={newQuantity}
                                onChange={(e) => setNewQuantity(e.target.value)}
                                className="bg-gray-900/50 border-gray-700 text-white placeholder:text-gray-500 focus-visible:ring-emerald-500/50"
                            />
                        </div>
                        <div className="md:col-span-2">
                            <select
                                value={newUnit}
                                onChange={(e) => setNewUnit(e.target.value)}
                                className="flex h-9 w-full rounded-md border border-gray-700 bg-gray-900/50 px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-emerald-500/50 text-white"
                            >
                                {units.map((u) => (
                                    <option key={u} value={u}>{u}</option>
                                ))}
                            </select>
                        </div>
                        <div className="md:col-span-3">
                            <select
                                value={newItemCategory}
                                onChange={(e) => setNewItemCategory(e.target.value)}
                                className="flex h-9 w-full rounded-md border border-gray-700 bg-gray-900/50 px-3 py-1 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-emerald-500/50 text-white"
                            >
                                {categories.map((cat) => (
                                    <option key={cat} value={cat}>{cat}</option>
                                ))}
                            </select>
                        </div>
                        <div className="md:col-span-1">
                            <Button type="submit" size="icon" className="w-full bg-emerald-600 hover:bg-emerald-700 text-white" disabled={saving}>
                                {saving ? <Loader2 className="w-5 h-5 animate-spin" /> : <Plus className="w-5 h-5" />}
                            </Button>
                        </div>
                    </form>
                </div>

                {/* Inventory List */}
                <div className="space-y-4">
                    <div className="flex items-center justify-between gap-4 bg-gray-800/30 p-4 rounded-xl border border-gray-700/30">
                        <div className="relative flex-1 max-w-sm">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                            <Input
                                placeholder="Search inventory..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="pl-9 bg-gray-900/50 border-gray-700 text-white placeholder:text-gray-500 focus-visible:ring-emerald-500/50"
                            />
                        </div>
                        <div className="text-gray-400 text-sm">
                            {filteredItems.length} items found
                        </div>
                    </div>

                    <div className="grid gap-4">
                        {filteredItems.length === 0 ? (
                            <div className="text-center py-12 text-gray-500 bg-gray-800/20 rounded-xl border border-gray-800 border-dashed">
                                <ShoppingBasket className="w-12 h-12 mx-auto mb-3 opacity-20" />
                                <p>No items found. Add some above!</p>
                            </div>
                        ) : (
                            filteredItems.map((item) => (
                                <div
                                    key={item.id}
                                    className="group flex items-center justify-between p-4 bg-gray-800/40 hover:bg-gray-800/60 border border-gray-700/50 hover:border-emerald-500/30 rounded-xl transition-all duration-300 backdrop-blur-sm"
                                >
                                    <div className="flex items-center gap-4 flex-1">
                                        <div className="w-10 h-10 rounded-full bg-emerald-900/30 flex items-center justify-center text-emerald-400 font-bold border border-emerald-500/20">
                                            {item.name.charAt(0).toUpperCase()}
                                        </div>
                                        <div className="flex-1">
                                            <h3 className="font-semibold text-gray-100">{item.name}</h3>
                                            <div className="flex items-center gap-2 text-xs text-gray-400 mt-1">
                                                <span className="px-2 py-0.5 rounded-full bg-gray-700/50 border border-gray-600">
                                                    {item.category}
                                                </span>
                                                <span className="text-gray-600">•</span>

                                                {editingId === item.id ? (
                                                    <div className="flex items-center gap-2 animate-in fade-in slide-in-from-left-2 duration-200">
                                                        <Input
                                                            value={editQuantity}
                                                            onChange={(e) => setEditQuantity(e.target.value)}
                                                            className="h-6 w-16 text-xs bg-gray-900 border-emerald-500/50 focus-visible:ring-0 px-2"
                                                            autoFocus
                                                            placeholder="Qty"
                                                        />
                                                        <select
                                                            value={editUnit}
                                                            onChange={(e) => setEditUnit(e.target.value)}
                                                            className="h-6 w-20 text-[10px] bg-gray-900 border border-emerald-500/50 rounded-sm focus-visible:outline-none text-white px-1"
                                                        >
                                                            {units.map((u) => (
                                                                <option key={u} value={u}>{u}</option>
                                                            ))}
                                                        </select>
                                                        <button onClick={() => saveEdit(item.id)} className="p-1 hover:text-emerald-400 transition-colors">
                                                            <Check className="w-3 h-3" />
                                                        </button>
                                                        <button onClick={cancelEditing} className="p-1 hover:text-red-400 transition-colors">
                                                            <X className="w-3 h-3" />
                                                        </button>
                                                    </div>
                                                ) : (
                                                    <button
                                                        onClick={() => startEditing(item)}
                                                        className="flex items-center gap-1 hover:text-emerald-400 transition-colors group/edit"
                                                        title="Click to edit quantity"
                                                    >
                                                        <span>{item.quantity} {item.unit}</span>
                                                        <Edit2 className="w-3 h-3 opacity-0 group-hover/edit:opacity-100 transition-opacity" />
                                                    </button>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        onClick={() => handleDeleteItem(item.id)}
                                        className="text-gray-500 hover:text-red-400 hover:bg-red-900/20 transition-colors"
                                        disabled={saving}
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </Button>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Inventory;
