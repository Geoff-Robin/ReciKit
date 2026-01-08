import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Leaf, Eye, EyeOff, Plus, X } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const Signup = () => {
  const navigate = useNavigate();
  const { toast } = useToast();

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    likes: "",
    allergies: "",
  });

  const [inventory, setInventory] = useState([
    { ingredient_name: "", quantity: "", unit: "grams" },
  ]);

  const addInventoryItem = () =>
    setInventory([...inventory, { ingredient_name: "", quantity: "", unit: "grams" }]);

  const updateInventoryItem = (index, field, value) => {
    const updated = [...inventory];
    updated[index][field] = value;
    setInventory(updated);
  };

  const removeInventoryItem = (index) => {
    setInventory(inventory.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match.");
      toast({
        title: "Error",
        description: "Passwords do not match",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);

    try {
      const form = new FormData();
      form.append("username", formData.name);
      form.append("email", formData.email);
      form.append("password", formData.password);
      form.append("likes", formData.likes);
      form.append("dislikes", formData.allergies);
      form.append("inventory", JSON.stringify(inventory));

      const baseUrl = (import.meta.env.VITE_BACKEND_URL || "").replace(/\/$/, "");
      const res = await fetch(baseUrl + "/api/auth/signup", {
        method: "POST",
        body: form,
        credentials: "include"
      });

      const data = await res.json();

      if (!res.ok) {
        if (data.detail === "User exists") {
          setError("That username is already taken. Please choose another.");
        } else {
          setError(data.detail || "Failed to create account. Please check your information.");
        }
        toast({
          title: "Error",
          description: data.detail || "Failed to create account",
          variant: "destructive",
        });
        return;
      }

      toast({
        title: "Success",
        description: "Account created successfully",
      });

      navigate("/home");
    } catch (err) {
      setError("Connection error. Could not reach the server.");
      toast({
        title: "Error",
        description: err?.message || "Server error",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-secondary to-background p-4">
      <div className="w-full max-w-md animate-fade-in">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-primary to-primary-glow mb-4 animate-glow">
            <Leaf className="w-8 h-8 text-primary-foreground" />
          </div>
          <h1 className="text-3xl font-bold text-foreground">Create Account</h1>
          <p className="text-muted-foreground mt-2">Join us today and get started</p>
        </div>

        <div className="bg-card rounded-2xl shadow-xl p-8 border border-border/50 backdrop-blur-sm">
          {error && (
            <div className="mb-6 p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive text-sm font-medium animate-in fade-in slide-in-from-top-1">
              {error}
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-2">
              <Label htmlFor="name">Username</Label>
              <Input id="name" value={formData.name} onChange={handleChange} required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" value={formData.email} onChange={handleChange} required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="likes">Likes</Label>
              <Input
                id="likes"
                type="text"
                placeholder="rice, beef, pasta"
                value={formData.likes}
                onChange={handleChange}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="allergies">Allergies</Label>
              <Input
                id="allergies"
                type="text"
                placeholder="nuts, dairy"
                value={formData.allergies}
                onChange={handleChange}
              />
            </div>
            <section className="mt-6">
              <div className="flex justify-between items-center mb-2">
                <h2 className="font-semibold">Inventory</h2>
                <Button type="button" variant="outline" onClick={addInventoryItem}>
                  <Plus className="w-4 h-4" /> Add
                </Button>
              </div>

              {inventory.map((item, i) => (
                <div key={i} className="flex gap-2 items-center mb-2">
                  <Input
                    value={item.ingredient_name}
                    placeholder="Ingredient"
                    onChange={(e) => updateInventoryItem(i, "ingredient_name", e.target.value)}
                  />

                  <Input
                    value={item.quantity}
                    placeholder="Qty"
                    type="number"
                    onChange={(e) => updateInventoryItem(i, "quantity", e.target.value)}
                  />

                  <select
                    value={item.unit}
                    onChange={(e) => updateInventoryItem(i, "unit", e.target.value)}
                    className="bg-background border rounded px-2 h-10"
                  >
                    <option value="grams">g</option>
                    <option value="kilograms">kg</option>
                    <option value="milliliters">ml</option>
                    <option value="liters">L</option>
                    <option value="pieces">pcs</option>
                  </select>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    onClick={() => removeInventoryItem(i)}
                    className="text-red-500 hover:text-red-700"
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </div>
              ))}
            </section>


            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={formData.password}
                  onChange={handleChange}
                  required
                  className="pr-10"
                />
                <button type="button" onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2">
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirmPassword">Confirm Password</Label>
              <div className="relative">
                <Input
                  id="confirmPassword"
                  type={showConfirmPassword ? "text" : "password"}
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                  className="pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2"
                >
                  {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>
            <Button type="submit" className="w-full" size="lg" disabled={loading}>
              {loading ? "Creating Account..." : "Create Account"}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link to="/login" className="text-primary font-semibold">Sign in</Link>
            </p>
          </div>
        </div>

        <p className="text-center text-xs text-muted-foreground mt-6">
          By signing up, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
};

export default Signup;
