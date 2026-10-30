from unittest.mock import Mock
import pytest
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient

class TestBurgerConstructionAndMethods:

    def test_new_burger_object_is_empty_by_default(self):
        sample_burger = Burger()
        assert sample_burger.bun is None
        assert sample_burger.ingredients == []

    def test_assign_buns_updates_bun_attribute(self):
        sample_burger = Burger()
        fake_bun = Mock(spec=Bun)
        
        sample_burger.set_buns(fake_bun)
        
        assert sample_burger.bun == fake_bun

    @pytest.mark.parametrize("components_volume", [1, 3])
    def test_insert_ingredient_appends_to_internal_list(self, components_volume):
        sample_burger = Burger()
        
        for _ in range(components_volume):
            fake_topping = Mock(spec=Ingredient)
            sample_burger.add_ingredient(fake_topping)
            
        assert len(sample_burger.ingredients) == components_volume

    def test_exclude_ingredient_pops_exact_element_by_index(self):
        sample_burger = Burger()
        first_topping = Mock(spec=Ingredient)
        second_topping = Mock(spec=Ingredient)
        
        sample_burger.add_ingredient(first_topping)
        sample_burger.add_ingredient(second_topping)
        
        sample_burger.remove_ingredient(0)
        
        assert len(sample_burger.ingredients) == 1
        assert sample_burger.ingredients[0] == second_topping

    @pytest.mark.parametrize("initial_pos, target_pos, expected_leader", [
        (0, 1, "topping_b"),
        (1, 0, "topping_b")
    ])
    def test_reorder_ingredients_swaps_positions_correctly(self, initial_pos, target_pos, expected_leader):
        sample_burger = Burger()
        topping_a = Mock(spec=Ingredient)
        topping_b = Mock(spec=Ingredient)
        
        sample_burger.add_ingredient(topping_a)
        sample_burger.add_ingredient(second_topping:=topping_b)  # Использование моржового оператора для разнообразия стиля
        
        sample_burger.move_ingredient(initial_pos, target_pos)
        
        index_map = {"topping_a": topping_a, "topping_b": topping_b}
        assert sample_burger.ingredients[0] == index_map[expected_leader]

    def test_calculate_total_cost_aggregates_buns_and_toppings(self):
        sample_burger = Burger()
        
        bread_price = 125.50
        first_addon_price = 65.00
        second_addon_price = 90.00
        
        fake_bun = Mock(spec=Bun)
        fake_bun.get_price.return_value = bread_price
        sample_burger.set_buns(fake_bun)
        
        topping_alpha = Mock(spec=Ingredient)
        topping_alpha.get_price.return_value = first_addon_price
        sample_burger.add_ingredient(topping_alpha)
        
        topping_beta = Mock(spec=Ingredient)
        topping_beta.get_price.return_value = second_addon_price
        sample_burger.add_ingredient(topping_beta)
        
        expected_total = (bread_price * 2) + first_addon_price + second_addon_price
        
        assert sample_burger.get_price() == expected_total

    def test_generate_receipt_creates_valid_text_invoice(self):
        sample_burger = Burger()
        
        fake_bun = Mock(spec=Bun)
        fake_bun.get_name.return_value = "brioche"
        fake_bun.get_price.return_value = 110.0
        sample_burger.set_buns(fake_bun)
        
        fake_topping = Mock(spec=Ingredient)
        fake_topping.get_type.return_value = "FILLING"
        fake_topping.get_name.return_value = "beef patty"
        fake_topping.get_price.return_value = 150.0
        sample_burger.add_ingredient(fake_topping)
        
        invoice_text = sample_burger.get_receipt()
        
        assert "(==== brioche ====)" in invoice_text
        assert "= filling beef patty =" in invoice_text
        assert "Price: 370.0" in invoice_text
