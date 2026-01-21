"""
Financial views.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Sum, Q

from core.common.permissions import IsFinanceManager
from .models import GroupCost, AdditionalSale, Commission, Invoice, BankDeposit
from .serializers import (
    GroupCostSerializer,
    AdditionalSaleSerializer,
    CommissionSerializer,
    InvoiceSerializer,
    InvoiceCreateSerializer,
    BankDepositSerializer
)


class GroupCostViewSet(viewsets.ModelViewSet):
    """GroupCost ViewSet."""

    queryset = GroupCost.objects.select_related('group', 'supplier').all()
    serializer_class = GroupCostSerializer
    permission_classes = [IsFinanceManager]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['group', 'supplier', 'cost_type', 'paid', 'currency']
    search_fields = ['description', 'invoice_number', 'group__code']
    ordering_fields = ['created_at', 'total_amount', 'payment_date']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get cost summary by group or cost type."""
        group_id = request.query_params.get('group')
        cost_type = request.query_params.get('cost_type')

        queryset = self.get_queryset()

        if group_id:
            queryset = queryset.filter(group_id=group_id)
        if cost_type:
            queryset = queryset.filter(cost_type=cost_type)

        summary = queryset.aggregate(
            total_costs=Sum('total_amount'),
            paid_costs=Sum('total_amount', filter=Q(paid=True)),
            pending_costs=Sum('total_amount', filter=Q(paid=False))
        )

        return Response(summary)


class AdditionalSaleViewSet(viewsets.ModelViewSet):
    """AdditionalSale ViewSet."""

    queryset = AdditionalSale.objects.select_related('passenger').all()
    serializer_class = AdditionalSaleSerializer
    permission_classes = [IsFinanceManager]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['passenger', 'sale_type', 'paid', 'currency']
    search_fields = ['description',
                     'passenger__first_name', 'passenger__last_name']
    ordering_fields = ['created_at', 'total_amount', 'payment_date']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def revenue(self, request):
        """Get additional sales revenue summary."""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        queryset = self.get_queryset()

        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        summary = queryset.aggregate(
            total_sales=Sum('total_amount'),
            paid_sales=Sum('total_amount', filter=Q(paid=True)),
            pending_sales=Sum('total_amount', filter=Q(paid=False))
        )

        return Response(summary)


class CommissionViewSet(viewsets.ModelViewSet):
    """Commission ViewSet."""

    queryset = Commission.objects.select_related('group').all()
    serializer_class = CommissionSerializer
    permission_classes = [IsFinanceManager]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['group', 'commission_type', 'paid', 'currency']
    search_fields = ['recipient_name', 'recipient_email', 'group__code']
    ordering_fields = ['created_at', 'commission_amount', 'payment_date']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def by_recipient(self, request):
        """Get commissions grouped by recipient."""
        recipient_email = request.query_params.get('email')

        if not recipient_email:
            return Response(
                {'error': 'Email parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset().filter(recipient_email=recipient_email)

        summary = queryset.aggregate(
            total_commissions=Sum('commission_amount'),
            paid_commissions=Sum('commission_amount', filter=Q(paid=True)),
            pending_commissions=Sum('commission_amount', filter=Q(paid=False))
        )

        summary['commissions'] = CommissionSerializer(queryset, many=True).data

        return Response(summary)


class InvoiceViewSet(viewsets.ModelViewSet):
    """Invoice ViewSet."""

    queryset = Invoice.objects.select_related('passenger').all()
    permission_classes = [IsFinanceManager]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['passenger', 'invoice_type',
                        'status', 'paid', 'currency']
    search_fields = ['invoice_number',
                     'customer_name', 'customer_document_number']
    ordering_fields = ['issue_date', 'total_amount', 'invoice_number']
    ordering = ['-issue_date']

    def get_serializer_class(self):
        """Return appropriate serializer for action."""
        if self.action == 'create':
            return InvoiceCreateSerializer
        return InvoiceSerializer

    @action(detail=True, methods=['post'])
    def send_to_sunat(self, request, pk=None):
        """Send invoice to SUNAT (placeholder for integration)."""
        invoice = self.get_object()

        if invoice.status != 'issued':
            return Response(
                {'error': 'Invoice must be in issued status to send to SUNAT'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # TODO: Implement actual SUNAT integration
        # For now, just update status
        invoice.status = 'sent'
        invoice.sunat_response = {
            'sent_at': timezone.now().isoformat(),
            'status': 'pending',
            'message': 'Sent to SUNAT - awaiting response'
        }
        invoice.save()

        return Response({
            'message': 'Invoice sent to SUNAT',
            'invoice': InvoiceSerializer(invoice).data
        })

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark invoice as paid."""
        invoice = self.get_object()

        payment_method = request.data.get('payment_method')
        payment_date = request.data.get('payment_date')

        if not payment_method or not payment_date:
            return Response(
                {'error': 'payment_method and payment_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        invoice.paid = True
        invoice.payment_method = payment_method
        invoice.payment_date = payment_date
        invoice.save()

        return Response(InvoiceSerializer(invoice).data)


class BankDepositViewSet(viewsets.ModelViewSet):
    """BankDeposit ViewSet."""

    queryset = BankDeposit.objects.select_related(
        'group', 'passenger', 'verified_by'
    ).all()
    serializer_class = BankDepositSerializer
    permission_classes = [IsFinanceManager]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['group', 'passenger',
                        'payment_method', 'status', 'currency']
    search_fields = ['reference_number', 'bank_name', 'group__code']
    ordering_fields = ['deposit_date', 'amount', 'created_at']
    ordering = ['-deposit_date']

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify a bank deposit."""
        deposit = self.get_object()

        if deposit.status == 'verified':
            return Response(
                {'error': 'Deposit is already verified'},
                status=status.HTTP_400_BAD_REQUEST
            )

        deposit.status = 'verified'
        deposit.verified_by = request.user
        deposit.verified_at = timezone.now()
        deposit.save()

        return Response(BankDepositSerializer(deposit).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a bank deposit."""
        deposit = self.get_object()

        if deposit.status == 'verified':
            return Response(
                {'error': 'Cannot reject a verified deposit'},
                status=status.HTTP_400_BAD_REQUEST
            )

        notes = request.data.get('notes', '')

        deposit.status = 'rejected'
        deposit.verified_by = request.user
        deposit.verified_at = timezone.now()
        deposit.notes = f"{deposit.notes}\n\nRejected: {notes}".strip()
        deposit.save()

        return Response(BankDepositSerializer(deposit).data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending deposits."""
        queryset = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
