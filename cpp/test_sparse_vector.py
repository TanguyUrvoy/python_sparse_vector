#!/usr/bin/env python

import unittest
import numpy
import random
import sys
from os.path import dirname, join
sys.path.append(join(dirname(__file__),"build"))

from sparse_vector import SparseVector, iSparseVector

def almost_equal(value_1, value_2, accuracy = 10**-6):
    return abs(value_1 - value_2) < accuracy


class TestSparseVector(unittest.TestCase):
    
    def test_empty_initialisation(self):
        sv = SparseVector()
        self.assertEqual("{}", str(sv))
        
    def test_initialisation_by_empty_list(self):
        sv = SparseVector([])
        self.assertEqual("{}", str(sv))
        
    def test_initialisation_by_list1(self):
        l = [random.random() for _ in range(1000)]
        sv = SparseVector(l)
        for i,v in enumerate(l):
            self.assertTrue(almost_equal(sv[i], v))
        
    def test_initialisation_by_list2(self):
        sv = SparseVector([1,2,3,4,5])
        self.assertEqual("{0:1,1:2,2:3,3:4,4:5}", str(sv))
        
    def test_initialisation_by_empty_dict(self):
        sv = SparseVector({})
        self.assertEqual("{}", str(sv))

    def test_initialisation_by_dict(self):
        sv = SparseVector({
            4: 6,
            3: 5,
        })
        self.assertEqual([0, 0, 0, 5, 6], sv.tolist())
        
    def test_initialisation_by_dict2(self):
        sv1 = SparseVector()
        sv2 = SparseVector({0:0, 1:0, 2:0})
        self.assertEqual(sv1, sv2)
        
        
    def test_initialisation_by_string(self):
        sv = SparseVector("7:1, 3:5 , 4:6, 6:0")
        self.assertEqual("{3:5,4:6,7:1}", str(sv))
        
    def test_initialisation_by_empty_string(self):
        sv = SparseVector("")
        self.assertEqual("{}", str(sv))
        
    def test_to_dict(self):
        sv = iSparseVector([1, 2, 3, 0, 5])
        self.assertEqual({0:1, 1:2, 2:3, 4:5} , sv.todict())
        
    def test_to_list(self):
        sv = iSparseVector({0:1, 1:2, 2:3, 5:5})
        self.assertEqual([1, 2, 3, 0, 0, 5], sv.tolist())
        

    def test_random_access_write(self):
        sv1 = SparseVector()
        N = 300
        indexes = [random.randint(0,100) for i in range(N)]
        values = [random.gauss(0,1) for i in range(N)]
        
        for i,v in zip(indexes,values):
            sv1[i] = v
            
        sv2 = SparseVector({ i:v for i,v in zip(indexes,values) })
        self.assertEqual(sv1, sv2)

    def test_random_access_read_present(self):
        sv = SparseVector()
        sv[0] = 1
        self.assertEqual(1, sv[0])

    def test_random_access_read_absent(self):
        sv = SparseVector()
        sv[1] = 12
        self.assertEqual(0, sv[0])

    def test_sparse_string_representations_int(self):
        sv = SparseVector()
        sv[3], sv[4] = 5, 6
        self.assertEqual('{3:5,4:6}', repr(sv))
        self.assertEqual('{3:5,4:6}', str(sv))

    def test_access_with_negative_index_with_no_value(self):
        sv = SparseVector()
        self.assertEqual(0, sv[-1])

#     def test_clone(self):
#         a = SparseVector([1, 2, 3])
#         b = a[:]
#         b.append(4)
#         self.assertEqual([1, 2, 3], a)
#         self.assertEqual([1, 2, 3, 4], b)

    def test_equality(self):
        a = SparseVector([1, 2, 3])
        b = SparseVector([1, 2, 3])
        self.assertTrue(a == b)
        self.assertTrue(not a != b)
        self.assertEqual(a, b)
        self.assertTrue(b == a)
        self.assertTrue(not b != a)
        self.assertEqual(b, a)
        
    def test_equality_denormalized(self):
        a = SparseVector({0:0})
        b = SparseVector({0:0, 1:0})
        self.assertTrue(a == b)
        self.assertTrue(not a != b)
        self.assertEqual(a, b)
        self.assertTrue(b == a)
        self.assertTrue(not b != a)
        self.assertEqual(b, a)        

    def test_inequality_same_length(self):
        a = SparseVector([1, 2, 3])
        b = SparseVector([1, 0, 3])
        self.assertTrue(a != b)
        self.assertTrue(not a == b)
        self.assertNotEqual(a, b)
        self.assertTrue(b != a)
        self.assertTrue(not b == a)
        self.assertNotEqual(b, a)

    def test_inequality_left_longer(self):
        a = SparseVector([1, 2, 3, 4])
        b = SparseVector([1, 2, 3])
        self.assertTrue(a != b)
        self.assertTrue(not (a == b))
        self.assertNotEqual(a, b)
        self.assertTrue(b != a)
        self.assertTrue(not (b == a))
        self.assertNotEqual(b, a)

    def test_leq(self):
        a = SparseVector([1, 2, 3, 0])
        b = SparseVector([1, 2, 4, 5])
        self.assertTrue(a <= b)
        self.assertFalse(a < b)
        self.assertFalse(a == b)
        self.assertFalse(a >= b)
        self.assertFalse(a > b)

    def test_geq(self):
        a = SparseVector([1, 2, 3, 0])
        b = SparseVector([1, 2, 4, 5])
        self.assertTrue(b >= a)
        self.assertFalse(b > a)
        self.assertFalse(b == a)
        self.assertFalse(b <= a)
        self.assertFalse(b < a)

#     def test_multiply(self):
#         sv = SparseVector({0: 1, 4: 1})
#         sv4 = sv * 4
#         self.assertEqual([1, 0, 0, 0, 1], sv)
#         self.assertEqual(
#             [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1], sv4)
#         self.assertEqual(len(sv) * 4, len(sv4))

#     def test_multiply_in_place(self):
#         sv = SparseVector({0: 1, 4: 1}, 0)
#         sv *= 4
#         self.assertEqual(
#             [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1], sv)

#     def test_count_value(self):
#         sv = SparseVector({0: 1, 4: 1}, 0)
#         self.assertEqual(2, sv.count(1))

#     def test_count_default_value(self):
#         sv = SparseVector(100, 1)
#         sv[5] = 1
#         self.assertEqual(100, sv.count(1))

#     def test_extend(self):
#         sv = SparseVector([1, 2, 3])
#         sv.extend((4, 5, 6))
#         self.assertEqual([1, 2, 3, 4, 5, 6], sv)

#     def test_index_value(self):
#         sv = SparseVector({0: 1, 4: 1}, 0)
#         self.assertEqual(0, sv.index(1))

#     def test_index_default_value(self):
#         sv = SparseVector({0: 1, 4: 1}, 0)
#         self.assertEqual(1, sv.index(0))

#     def test_index_absent_default_value(self):
#         sv = SparseVector([1, 2, 3], 0)
#         self.assertRaises(ValueError, sv.index, 0)

#     def test_index_absent_value(self):
#         sv = SparseVector(1, 0)
#         self.assertRaises(ValueError, sv.index, 2)

#     def test_pop_no_value(self):
#         sv = SparseVector(4)
#         self.assertEqual(0, sv.pop())

#     def test_pop_empty(self):
#         sv = SparseVector(0)
#         self.assertRaises(IndexError, sv.pop)

#     def test_pop_value(self):
#         sv = SparseVector([1, 2, 3])
#         popped = sv.pop()
#         self.assertEqual(3, popped)
#         self.assertEqual(2, len(sv))
#         self.assertEqual([1, 2], sv)

#     def test_push_value(self):
#         sv = SparseVector([1, 2, 3])
#         sv.push(4)
#         self.assertEqual(4, len(sv))
#         self.assertEqual([1, 2, 3, 4], sv)

#     def test_remove_value(self):
#         sv = SparseVector([1, 2, 3])
#         sv.remove(2)
#         self.assertEqual(3, len(sv))
#         self.assertEqual([1, 0, 3], sv)

#     def test_remove_only_first_value(self):
#         sv = SparseVector([2, 2, 3])
#         sv.remove(2)
#         self.assertEqual(3, len(sv))
#         self.assertEqual([0, 2, 3], sv)

#     def test_remove_non_value(self):
#         sv = SparseVector([1, 2, 3])
#         self.assertRaises(ValueError, sv.remove, 4)

#     def test_remove_default_value_does_nothing(self):
#         sv = SparseVector(4, default_value=1)
#         sv.remove(1)
#         self.assertEqual([1, 1, 1, 1], sv)
        
        

if __name__ == '__main__':
    unittest.main()
