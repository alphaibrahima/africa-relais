from django.urls import path, include

from dash.views import team
from dash.views import shared
from dash.views import professionnal
from dash.views import particular
from dash.views import deliverman
from dash.views import staff
from dash.views import realypoint


app_name = "dashboard"

urlpatterns = [
    path("dashboard/", shared.dashboard_view, name="dashboard"),
    path("dashboard/notifications/", shared.get_notifications, name="notifications"),
    path(
        "staff/",
        include(
            [
                path("dashboard/", staff.dashboard, name="staff-dashboard"),
                path("profile/", staff.user_update, name="staff-profile"),
                path("team/", staff.team_member, name="team-member"),
                path("professional/", staff.pro_member, name="pro-member"),
                path("pack/", staff.pack_management, name="pack-management"),
                path("users/", staff.user_management, name="user-management"),
                path(
                    "users/<int:relay_id>/activate/",
                    staff.desactivate_realypoint,
                    name="activate_realypoint_account",
                ),
                path(
                    "users/<int:user_id>/deactivate/",
                    staff.deactivate_user_account,
                    name="deactivate-user-account",
                ),
                path(
                    "users/<int:user_id>/activate/",
                    staff.activate_user_account,
                    name="activate-user-account",
                ),
                path("bills/", staff.bill_management, name="bill-management"),
                path("packages/", staff.package_management, name="package-management"),
                path("contacts/", staff.contact_management, name="contact-management"),
                path(
                    "deliveries/", staff.delivery_management, name="delivery-management"
                ),
                path(
                    "deliverymen/",
                    staff.delivery_man_management,
                    name="delivery_man_management",
                ),
                path("coupons/", staff.coupons, name="coupon-list"),
                path(
                    "realypoint/",
                    staff.realypoint_management,
                    name="realypoint-management",
                ),
                path(
                    "relaypoint/update/<int:pk>",
                    staff.update_realypoint,
                    name="staff-update-relaypoint",
                ),
                path(
                    "team/update/<int:pk>",
                    staff.update_team,
                    name="staff-update-team",
                ),
                path(
                    "users/update/<int:pk>",
                    staff.update_user,
                    name="staff-update-user",
                ),
                path(
                    "team/delete/<int:pk>",
                    staff.delete_team_member,
                    name="staff-delete-team",
                ),
                path(
                    "relaypoint/delete/<int:pk>",
                    staff.delete_relaypoint,
                    name="staff-delete-relaypoint",
                ),
                path(
                    "relay-points/<int:relay_point_id>/rates",
                    staff.relay_point_rate,
                    name="relay-point-rate",
                ),
                path(
                    "relay-points/points/upload",
                    staff.test_upload_departure_arrival,
                    name="test_upload_departure_arrival",
                ),
                path(
                    "deliverymen/update/<int:pk>",
                    staff.update_deliverymen,
                    name="staff-update-deliverymen",
                ),
                path(
                    "users/<int:user_id>/delete/",
                    staff.delete_user_account,
                    name="delete-user-account",
                ),
            ]
        ),
    ),
    path(
        "professionnal/",
        include(
            [
                path(
                    "dashboard/",
                    professionnal.dashboard,
                    name="professionnal-dashboard",
                ),
                path(
                    "profile/", professionnal.user_update, name="professionnal-profile"
                ),
                path(
                    "address-book/",
                    professionnal.address_book_list,
                    name="professionnal-address-book",
                ),
                path(
                    "account/",
                    professionnal.address_book_list,
                    name="professionnal-account",
                ),
                path(
                    "packages/",
                    professionnal.package_list,
                    name="professionnal-package-list",
                ),
                path("relypoint-list/", professionnal.rely_list, name="relypoint_list"),
                path(
                    "revenus/",
                    professionnal.revenus_list,
                    name="professionnal-revenus-list",
                ),
                path(
                    "paiement-compte/",
                    professionnal.paiement_pro,
                    name="paiement_pro",
                ),
                path(
                    "choix-paiement/",
                    professionnal.choice_pro,
                    name="choice_pay_pro",
                ),
                path(
                    "paiement-bancaire/",
                    professionnal.bancaire_pro,
                    name="bank_pay_pro",
                ),
                path(
                    "paiement-wave/",
                    professionnal.wave_pro,
                    name="paiement-wave_pro",
                ),
                path(
                    "paiement-orange-money/",
                    professionnal.orange_pro,
                    name="paiement-orange-money_pro",
                ),
                path(
                    "paiement-free-money/",
                    professionnal.free_pro,
                    name="paiement-free-money_pro",
                ),
                path(
                    "paiement-paydunya/",
                    professionnal.dunya_pro,
                    name="pro_dunya",
                ),
            ]
        ),
    ),
    # url particular
    path(
        "particular/",
        include(
            [
                path(
                    "dashboard/",
                    particular.dashboard,
                    name="particular-dashboard",
                ),
                path("profile/", particular.user_update, name="particular-profile"),
                path(
                    "packages/",
                    particular.package_list,
                    name="particular-package-list",
                ),
                path(
                    "revenus/",
                    particular.revenus_list,
                    name="particular-revenus-list",
                ),
                path(
                    "address-book/",
                    particular.address_book_list,
                    name="particular-address-book",
                ),
                path(
                    "bill_list/",
                    particular.bill_list,
                    name="particular-bill-list",
                ),
                path(
                    "bill/<str:pk>/",
                    particular.bill,
                    name="particular-bill",
                ),
                path(
                    "bill/<int:bill_id>/pdf/",
                    particular.pdf,
                    name="particular-bill-to-pdf",
                ),
                path(
                    "express-service/",
                    particular.express,
                    name="express",
                ),
                path(
                    "paiement-compte/",
                    particular.paiement_part,
                    name="paiement",
                ),
                path(
                    "choice-paiement/",
                    particular.choice,
                    name="choice_pay",
                ),
                path(
                    "paiement-wave/",
                    particular.wave,
                    name="paiement-wave",
                ),
                path(
                    "paiement-bancaire/",
                    particular.bancaire,
                    name="bank_pay",
                ),
                path(
                    "paiement-orange-money/",
                    particular.orange,
                    name="paiement-orange-money",
                ),
                path(
                    "paiement-free-money/",
                    particular.free,
                    name="paiement-free-money",
                ),
                path(
                    "paiement-paydunya/",
                    particular.dunya,
                    name="paiement-dunya",
                ),
            ]
        ),
    ),
    path(
        "team/",
        include(
            [
                path(
                    "dashboard/",
                    team.dashboard,
                    name="team-dashboard",
                ),
                path("profile/", team.user_update, name="team-profile"),
                path(
                    "users/<int:user_id>/deactivate/",
                    team.deactivate_user_account,
                    name="team-deactivate-user-account",
                ),
                path(
                    "address-book/",
                    team.address_book_list,
                    name="team-address-book",
                ),
                path(
                    "packages/",
                    team.package_list,
                    name="team-package-list",
                ),
                path(
                    "revenus/",
                    team.revenus_list,
                    name="team-revenus-list",
                ),
                path(
                    "relaypoint/",
                    team.relay_point,
                    name="team-relaypoint-liste",
                ),
                path(
                    "relaypoint/update/<int:pk>",
                    team.update_realypoint,
                    name="team-update-relaypoint",
                ),
                path(
                    "relaypoint/delete/<int:pk>",
                    team.delete_realypoint,
                    name="team-delete-relaypoint",
                ),
                path(
                    "deliverman/",
                    team.deliverman,
                    name="team-deliverman-list",
                ),
            ]
        ),
    ),
    path(
        "deliverman/",
        include(
            [
                path(
                    "dashboard/",
                    deliverman.DelivermanDashboard,
                    name="dashboard-deliverman",
                ),
                path("profile/", deliverman.user_update, name="deliverman-profile"),
                path("revenue/", deliverman.revenue, name="deliverman-revenue"),
                path(
                    "address-book/",
                    deliverman.AddressBookView.as_view(),
                    name="deliverman-address-book",
                ),
                path(
                    "list-realypoint/",
                    deliverman.realypoint_list,
                    name="deliverman-realypoint_list",
                ),
                path("history/", deliverman.history, name="deliverman-history-list"),
                path(
                    "relaypoint/",
                    team.relay_point,
                    name="team-relaypoint-list",
                ),
                path(
                    "deliverman/",
                    team.deliverman,
                    name="team-deliverman-list1",
                ),
            ]
        ),
    ),
    # url realypoint
    path(
        "realypoint/",
        include(
            [
                path("dashboard/", realypoint.dashboard, name="dashboard-realypoint"),
                path("profile/", realypoint.profile, name="realypoint-profile"),
                path("package/", realypoint.package, name="realypoint-package"),
                path("revenue/", realypoint.revenue, name="realypoint-revenue"),
                path("horaire/", realypoint.schedule, name="realypoint-horaire"),
            ]
        ),
    ),
]
